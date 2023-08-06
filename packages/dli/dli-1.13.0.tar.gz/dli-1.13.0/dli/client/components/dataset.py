#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import inspect
import logging
import warnings

from dli.client.builders import DatasetBuilder
from dli.client.components import SirenComponent, SirenAdapterResponse
from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.client.utils import ensure_count_is_valid
from dli.models.dictionary_model import DictionaryModel
from dli.siren import siren_to_entity

from dli.client.components.urls import dataset_urls, consumption_urls, \
    package_urls

class Dataset(SirenComponent):

    def get_s3_access_keys_for_dataset(self, *dataset_ids):
        """
        Retrieve S3 access keys for the specified account to access the
        specified dataset(s).

        :param list dataset_ids: One ore more dataset ids to get access to.
        :returns: A namedtuple containing the AWS keys and session token.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                s3_access_keys = client.get_s3_access_keys_for_dataset(dataset_id1, dataset_id2)
                # print(s3_access_keys)
                # access_key(access_key_id='39D19A440AFE452B9', secret_access_key='F426A93CDECE45C9BFF8F4F19DA5CB81', session_token='C0CC405803F244CA99999')

        """


        payload = {"datasetIds": list(dataset_ids)}

        response = self.session.post(
            dataset_urls.access_keys, json=payload
        )

        return siren_to_entity(SirenAdapterResponse(response).to_siren())

    def get_dataset(self, id=None, name=None, package_id=None, package_name=None,
            dataset_short_code=None, organisation_short_code=None):
        """
        Retrieves a dataset.

        :param str id: The id of the dataset.
        :param str name: The name of the dataset.
        :param str package_id: The id of the package to which this dataset belongs.
                            Either this or package name is required if dataset is being looked up by name.
        :param str package_name: The name of the package to which this dataset belongs.
                            Either this or package id is required if dataset is being looked up by name.
        :param str dataset_short_code: Optional field. The short code of the requested dataset.
                            Should be used with organisation_short_code.
        :param str organisation_short_code: Optional field.
                            The short code of the organisation the requested dataset belongs to.
                            Needs to be used together with dataset_short_code.
                            If not specified, and dataset_short_code is defined,
                            then datasets will be searched within requesting user organisation.

        :returns: The dataset.
        :rtype: Dataset

        - **Sample**

        .. code-block:: python

                # Look up by dataset short code
                dataset = client.get_dataset(dataset_short_code='my_dataset_id')
                # or
                dataset = client.get_dataset(dataset_short_code='my_dataset_short_code', organisation_short_code='some_org_short_code')
                # Look up by dataset id
                dataset = client.get_dataset('my_dataset_id')
                # or equivalent
                dataset = client.get_dataset(id='my_dataset_id')

                # Look up by dataset name

                # If package id is known
                dataset = client.get_dataset(name='my_dataset', package_id='my_package_id')

                # if package name is known
                dataset = client.get_dataset(name='my_dataset', package_name='my_package')
        """
        caller = inspect.stack()[2]
        if caller.function.startswith("<module>") or \
                ("/dli/tests/" in caller.filename and caller.function.startswith("test_direct")):
            warnings.warn(
                'This method is deprecated and is scheduled for removal in '
                'dli=1.13.0. '
                '\nTo get a dataset, please use the alternate calls:'
                '\n'
                '\n    import dli'
                '\n    client = dli.connect()'
                '\n    dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)'
                '\n'
                '\nor:'
                '\n'
                '\n    import dli'
                '\n    client = dli.connect()'
                '\n'
                '\n    # When you do not know the dataset short code and want to search,'
                '\n    # then there may be multiple matches returned.'
                '\n    # Return type: OrderedDict[id: str, DatasetModel]'
                '\n    datasets = client.datasets(search_term=["name=<dataset_name>"])'
                '\n'
                '\nWhen you have found your dataset, then you can perform operations on the '
                'dataset such as:'
                '\n'
                '\n    dataset.partitions()'
                '\n'
                '\nFor more details please refer to '
                'https://supportlibrary.ihsmarkit.com/display/DLSL/Using+a+Dataset',
                PendingDeprecationWarning
            )

        if dataset_short_code:
            response = self.session.get(
                dataset_urls.v2_by_short_code.format(
                    dataset_short_code=dataset_short_code
                ), params={'organisation_short_code': organisation_short_code}
            )

        elif organisation_short_code and not id:
            # Incidentally dataset ID also works with organisation_short_code
            # but as it's deprecated it is not recommended for use.
            raise Exception("Specify the dataset_short_code "
                            "with the organisation_short_code.")

        else:
            if not id and name and (package_name or package_id):
                id = self._get_dataset_id_by_name(
                    dataset_name=name,
                    package_id=package_id,
                    package_name=package_name
                )
            elif name and not (package_name or package_id):
                # we have no way to get the ID.
                raise Exception("Package name or package ID must be provided"
                                " along with the dataset name in order to"
                                " retrieve a dataset by name. "
                                "It is preferable to use "
                                "dataset_short_code and "
                                "organisation_short_code.")
            elif not name and not id:
                raise Exception("You must provide the dataset_id (id=) or the"
                                "dataset_name (name=) alongside the "
                                "package name or package ID.")

            response = self.session.get(
                dataset_urls.v2_by_id.format(id=id)
            )

        return self._DatasetFactory._from_v2_response(response.json(), warn=True)

    def _get_dataset_id_by_name(self, package_id=None,
                                dataset_name=None,
                                package_name=None):
        if dataset_name and package_name:
            params = {"name": package_name}

            p = self.packages(search_term=[f"name={package_name}"])
            if len(p) == 1:
                package_id = p[package_name].id
            else:
                raise CatalogueEntityNotFoundException("No such package")

        ds = self.datasets(search_term=[f"package_id={package_id}",
                                        f"name={dataset_name}"], warn=False)
        try:
            return next(iter(ds.values())).id
        except StopIteration as s:
            raise Exception(f"No such dataset `{dataset_name}`")

    def register_dataset(self, builder: DatasetBuilder):
        """
        Submit a request to create a new dataset under a specified package in the Data Catalogue.

        :param dli.client.builders.DatasetBuilder builder: An instance of DatasetBuilder. This builder object sets sensible defaults and exposes
                                                           helper methods on how to configure its storage options.

        :returns: A newly created Dataset.
        :rtype: Dataset

        - **Sample**

        .. code-block:: python

                # Please refer to builder docs for examples on
                # how to create an instance of DatasetBuilder.

                dataset = client.register_dataset(builder)
        """
        mp_encoder = builder.to_multipart_body()

        result = self.session.post(
            dataset_urls.v2_index,
            data=mp_encoder,
            headers={
                'Content-Type': mp_encoder.content_type,
                'Content-Length': str(mp_encoder.len),
            },
        ).json()

        return self._DatasetFactory._from_v2_response(result)

    def edit_dataset(
        self,
        dataset_id,
        location_builder=None,
        **kwargs
    ):
        """
        Updates information on a dataset, returning the updated instance.
        If keyword argument is not specified field keeps its old value.
        Optional enum and text type fields can be unset by passing ``None``.

        :param str dataset_id: Id of the dataset being updated.
        :param dli.client.builders.DatasetLocationBuilder location_builder: Optional. An instance of DatasetLocationBuilder. This builder object exposes
                                                                            helper methods to configure dataset storage options.

        Keyword arguments:

        :keyword str name: Optional. A descriptive name of a dataset. It should be unique within the package.
        :keyword str description: Optional. A short description of a package.
        :keyword str content_type: Optional. A way for the data steward to classify the type of data in the dataset
                                (e.g. Structured or Unstructured).
        :keyword str data_format: Optional. The format of the data: `CSV`, `IMAGE`, `JSON`, `PARQUET`, `TXT`, `TSV`, XML`, `Other`.
        :keyword str publishing_frequency: Optional. The internal on which data is published. Possible values are: `Hourly`,
                                        `Daily`, `Weekday`, `Weekly`, `Monthly`, `Quarterly`, `Yearly`, `Not Specified`.
        :keyword list[str] keywords: Optional. User-defined list of keywords that can be used to find this dataset through
                                    the search interface.
        :keyword str naming_convention: Optional. Key for how to read the dataset name.
        :keyword str documentation: Optional. Documentation about this dataset in markdown format.
        :keyword list[str] taxonomy: Optional. A list of segments to be used for a taxonomy,
                                    the Data-<< Organization >>-<< topic >> prefix will be applied by the catalogue  For
                                    a taxonomy of Data-IHS Markit-Financial Markets-Credit-CDS, you would provide
                                    `taxonomy=["Credit", "CDS"]`
        :keyword str load_type: Optional. Whether each datafile in this dataset should be considered as a full version
                                of a dataset or a delta or increment. Accepted types are `Full Load`, `Incremental Load`
        :keyword str data_preview_type: Optional enum of NONE STATIC LIVE. 'NONE' means there is no datapreview. STATIC means
                            to use the file provided. LIVE means to use the latest datafile.
        :keyword file sample_data: Optional file. File like object. Used in conjuntion with data_preview_type. Max size 10Megabytes.

        :returns: Updated Dataset.
        :rtype: Dataset

        - **Sample**

        .. code-block:: python

                # e.g. update dataset description
                updated_dataset = client.edit_dataset(
                    "my-dataset-id",
                    description="Updated my dataset description"
                )

                # update dataset location. Please note that this is only allowed if the dataset has no datafiles registered.
                builder = DatasetLocationBuilder().with_external_storage("external-storage-location")
                updated_dataset = client.edit_dataset(
                    "my-dataset-id",
                    location_builder=builder
                )

                # update dataset taxonomy
                updated_dataset = client.edit_dataset(
                    "my-dataset-id",
                    taxonomy=["Credit", "CDS"]
                )

        """
        builder = DatasetBuilder(
            location_builder=location_builder,
            **kwargs
        )

        mp_encoder = builder.to_multipart_body()
        result = self.session.patch(
            dataset_urls.v2_by_id.format(id=dataset_id), data=mp_encoder,
            headers={
                'Content-Type': mp_encoder.content_type,
                'Content-Length': str(mp_encoder.len),
            }
        ).json()

        return self._DatasetFactory._from_v2_response(result)

    def delete_dataset(self, dataset_id):
        """
        Marks a particular dataset (and all its datafiles) as deleted.
        This dataset will no longer be accessible by consumers.

        :param str dataset_id: The id of the dataset to be deleted.

        :returns: None

        - **Sample**

        .. code-block:: python

                client.delete_dataset(dataset_id)

        """
        self.session.delete(
            dataset_urls.v2_by_id.format(id=dataset_id)
        )

    def get_datafiles(self, dataset_id, name_contains=None,
                      as_of_date_start=None, as_of_date_end=None,
                      page=1, count=100):
        """
        Returns a list of all datafiles registered under a dataset.

        :param str dataset_id: The id of the dataset.
        :param str name_contains: Optional. Look up only those datafiles for the dataset where name contains this string.
        :param str as_of_date_start: Optional. Datafiles having data_as_of date greater than or equal to this date. This must be specified in YYYY-MM-DD format.
        :param str as_of_date_end: Optional. Datafiles having data_as_of date less than or equal to this date. This must be specified in YYYY-MM-DD format.
        :param int count: Optional count of datafiles to be returned. Defaults to 100.

        :returns: List of all datafiles registered under the dataset.
        :rtype: List[Datafile]

        - **Sample**

        .. code-block:: python

                datafiles = client.get_datafiles(
                    dataset_id,
                    name_contains='My Test Data',
                    as_of_date_start='2018-10-11',
                    as_of_date_end='2018-10-15',
                    count=10
                )
        """

        ensure_count_is_valid(count)

        params = {
            'name': name_contains,
            'as_of_date_start': as_of_date_start,
            'as_of_date_end': as_of_date_end,
            'page_size': count,
            'page': page,
        }

        return SirenAdapterResponse(
            self.session.get(
                dataset_urls.datafiles.format(id=dataset_id), params=params
            )
        ).to_many_siren('datafile')

    def get_latest_datafile(self, dataset_id):
        """
        Fetches datafile metadata of latest datafile in the dataset.

        :param str dataset_id: The id of the dataset.

        :returns: The datafile.
        :rtype: Datafile

        - **Sample**

        .. code-block:: python

                datafile = client.get_latest_datafile(dataset_id)
        """
        datafile = SirenAdapterResponse(
            self.session.get(
                dataset_urls.latest_datafile.format(id=dataset_id)
            )
        ).to_siren()

        return siren_to_entity(datafile)


class Dictionary(SirenComponent):

    def register_dictionary(
        self,
        dataset_id,
        version,
        valid_as_of,
        fields,
        **kwargs
    ):
        """
        Registers dictionary metadata for a dataset.

        :param str dataset_id: Id of the dataset for the dictionary.
        :param str version: A user assigned version name/number. It should be unique within the dataset.
        :param str valid_as_of: The date as of which the dictionary is active.
                               Expected format is YYYY-MM-DD. Must be unique.
        :param list[dict] fields: Non empty list of `Field` as described below.
        :param list[dict] partitions: Optional. Non empty list of `Partition` as described below.
        :param str description: Optional. Description for the dictionary.

        :returns: The registered dictionary

        Types
        =====

        Dictionary Field:

        .. code-block:: python

            {
                name	        string  - required
                type	        string  - required
                nullable        boolean - required
                metadata	dictionary
                description	string
                sample_value	string
                short_name	string
                is_derived	boolean
                validation	string
                comment	        string
            }

        Partition:

        .. code-block:: python

            {
                name: string,
                type: string
            }

        - **Sample**

        .. code-block:: python

                my_dictionary_fields = [
                            {
                                'name': 'field_1',
                                'type': 'String',
                                'nullable': False
                            },
                            {
                                'name': 'field_2',
                                'type': 'Double',
                                'nullable': False
                            },
                            {
                                'name': 'field_3',
                                'type': 'Int',
                                'nullable': True,
                                'metadata': {
                                    'some_key': 'some_value'
                                }
                            },
                        ]
                my_dictionary_partitions = [
                    {
                        'name': 'field_1',
                        'type': 'String'
                    }
                ]

                my_dictionary = client.register_dictionary(
                    "my-dataset-id",
                    version='1a',
                    valid_as_of='2018-10-31',
                    fields=my_dictionary_fields,
                    partitions=my_dictionary_partitions,
                    description="My dictionary description"
                )
        """
        payload = {
            'dataset_id': dataset_id,
            'version': version,
            'valid_as_of': valid_as_of,
            'fields': fields,
        }

        payload.update(**kwargs)

        response = self.session.post(
            dataset_urls.dictionary_index, json={'data': {'attributes': payload}}
        )

        return DictionaryModel(response.json()['data'], client=self)

    def get_dictionary(self, dataset_id, version=None):
        """
        Looks up dictionary for a dataset by version. In case version is not specified this will fetch dictionary version having the latest valid_as_of date.
        Throws exception if no dictionary is registered for the dataset.

        :param str dataset_id: The id of the dataset under which the dictionary is registered.
        :param str version: Optional. The version of the dictionary.

        :returns: The dictionary.

        - **Sample**

        .. code-block:: python

                # Fetch dictionary version '1a'
                dictionary = client.get_dictionary('my_dataset_id', version='1a')

                # Fetch the dictionary with the latest valid_as_of date
                latest_dictionary = client.get_dictionary('my_dataset_id')

        """

        if version:
            schema = self.session.get(
                dataset_urls.v2_schema_instance_version.format(
                    id=dataset_id,
                    version=version
                )
            )
        else:
            schema = self.session.get(
                dataset_urls.dictionary_by_dataset_lastest.format(
                    id=dataset_id
                )
            )
        json = schema.json()['data']
        return DictionaryModel(json, client=self)

    def get_dictionaries(self, dataset_id, count=100):
        """
        Returns a list of all dictionaries registered under the dataset. The list is sorted by dictionary valid_as_of date in descending order.

        :param str dataset_id: The id of the dataset.
        :param int count: Optional count of dictionaries to be returned. Defaults to 100.

        :returns: List of all dictionaries registered under the dataset sorted by valid_as_of date in descending order.

        - **Sample**

        .. code-block:: python

                my_dictionaries = client.get_dictionaries("my_dataset_id", count=10)
        """
        response = self.session.get(
            dataset_urls.dictionary_by_dataset.format(id=dataset_id)
        )

        return [
            DictionaryModel(d, client=self) for d in
            response.json()['data']
        ][:count]  # todo - will kill this silly count stuff ASAP

    def delete_dictionary(self, dataset_id, version):
        """

        Marks a dictionary version for a dataset as deleted.

        :param str dataset_id: The id of the dataset under which the dictionary is registered.
        :param str version: The version of the dictionary.

        :returns: None

        - **Sample**

        .. code-block:: python

                # Delete dictionary version '1a'
                client.delete_dictionary(dataset_id='my_dataset_id', version='1a')

        """
        schema = self.get_dictionary(dataset_id, version)
        self.session.delete(
            dataset_urls.dictionary_instance.format(id=schema.id)
        )

    def edit_dictionary(
        self,
        dataset_id,
        version,
        new_version=None,
        **kwargs
    ):
        """
        Updates dictionary metadata for a dataset.
        If a field is passed as ``None`` then the field will not be updated.

        :param str dataset_id: Id of the dataset for the dictionary_instance.
        :param str version: Version of the dictionary being updated.
        :param str new_version: Optional. New version if to be updated. This is a user assigned version name/number. It should be unique within the dataset.
        :param str valid_as_of: Optional. The date as of which the dictionary is active.
                               Expected format is YYYY-MM-DD.
        :param list[dict] fields: Optional. If provided, a non empty list of `Field` as described below.
        :param list[dict] partitions: Optional. If provided, a non empty list of `Partition` as described below.
        :param str description: Optional. Description for the dictionary.

        .. code-block:: python

                # Field:
                {
                    "name": "field_a", 			# name of the column.
                    "nullable": True,  			# defaulted to True - A boolean indicating whether the field is nullable or not.
                    "metadata": None			# optional dictionary with metadata for this column.
                }

                # Partition:
                {
                    "name": "key1",
                    "type": "String"
                }

        :returns: The updated dictionary.
        :rtype: dli.models.dictionary_model.DictionaryModel

        - **Sample**

        .. code-block:: python

                # Updating description and valid_as_of date for my dictionary
                my_updated_schema = client.edit_dictionary(
                    "my-dataset-id",
                    '1a',
                    valid_as_of='2018-11-05',
                    description="My updated dictionary description"
                )
        """
        schema = self.get_dictionary(dataset_id, version)
        payload = dict(**kwargs)

        if new_version is not None:
            payload['version'] = new_version

        response = self.session.patch(
            dataset_urls.dictionary_instance.format(id=schema.id),
            json={'data': {'attributes': payload}}
        )

        return DictionaryModel(response.json()['data'], client=self)