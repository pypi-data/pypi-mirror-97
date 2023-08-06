#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import copy
import os
import json

from requests_toolbelt.multipart.encoder import MultipartEncoder

TEN_MEGABYTES = 10485760

class DatasetBuilder:
    """
    Dataset is grouping of related datafiles. It provides user with metadata required to consume and use the data.

    This builder object sets sensible defaults and exposes
    helper methods on how to configure its storage options..

    :param str package_id: Package ID to which the dataset belongs to.
    :param str name: A descriptive name of the dataset. It should be unique within the package the dataset
                    belongs to.
    :param str description: A short description of the dataset.
    :param str content_type: A way for the data steward to classify the type of data in the dataset
                        (e.g. Structured or Unstructured).
    :param str data_format: The format of the data: `CSV`, `IMAGE`, `JSON`, `PARQUET`, `TXT`, `TSV`,`XML`, `Other`.
    :param str publishing_frequency: The internal on which data is published. Possible values are: `Hourly`,
                                        `Daily`, `Weekday`, `Weekly`, `Monthly`, `Quarterly`, `Yearly`, `Not Specified`.
    :param list[str] taxonomy: A list of segments to be used for a taxonomy,
                                    the Data-<< Organization >>-<< topic >> prefix will be applied by the catalogue  For
                                    a taxonomy of Data-IHS Markit-Financial Markets-Credit-CDS, you would provide
                                    `taxonomy=["Credit", "CDS"]`
    :param str short_code: Optional. A short code for the dataset, should be an alphanumerical camel-cased string.
                        If not provided, a short_code will be generated based on the name.
    :param list[str] keywords: Optional. User-defined list of separated keywords that can be used to find this dataset
                            through the search interface.
    :param str naming_convention: Optional. Key for how to read the dataset name.
    :param str documentation: Optional. Documentation about this dataset in markdown format.
    :param str load_type: Optional. Whether each datafile in this dataset should be considered as a full version of a
                        dataset or a delta or increment. Accepted types are `Full Load`, `Incremental Load`
    :param str has_datafile_monitoring: Optional. Notify when latest instance is missing

    # XXX
    :param str data_preview_type: Optional enum of NONE STATIC LIVE. 'NONE' means there is no datapreview. STATIC means to use the file provided. LIVE means to use the latest datafile.
    :param file sample_data: Optional file. File like object. Used in conjuntion with data_preview_type.
    """

    @staticmethod
    def _create_dliv1_paylod(
        package_id=None,
        name=None,
        description=None,
        content_type=None,
        data_format=None,
        publishing_frequency=None,
        taxonomy=None,
        keywords=None,
        naming_convention=None,
        documentation=None,
        load_type=None,
        **kwargs
    ):
        return {
            "packageId": package_id,
            "name": name,
            "description": description,
            "keywords": keywords,
            "contentType": content_type,
            "location": None,
            "dataFormat": data_format,
            "publishingFrequency": publishing_frequency,
            "namingConvention": naming_convention,
            "documentation": documentation,
            "taxonomy": taxonomy,
            "loadType": load_type
        }

    def __init__(self, location_builder=None, **kwargs):
        self._data = dict(kwargs)

        self._data['sample_data'] = self._data.get('sample_data')
        if self._data.get('sample_data'):
            self._data['data_preview_type'] = (
                    self._data.get('data_preview_type') or 'STATIC'
            )
            self._validate_preview_type_static(
                self._data.get('data_preview_type')
            )

        # this is just for DLI v1 TODO add deprecated to it.
        self.payload = self._create_dliv1_paylod(**self._data)
        self._location_builder = location_builder

    def to_json_api(self):
        attributes = dict(**self._data)
        if self._location_builder is not None:
            attributes.update(**self._location_builder._dliv2())

        # This is a file
        attributes.pop('sample_data', None)
        return {
            'type': 'dataset',
            'data': {'attributes': attributes}
        }

    def to_multipart_body(self):
        data = json.dumps(self.to_json_api())

        fields={
            'data': ('data', data, 'application/json'),
        }

        if self._data['sample_data']:
            fields['sample_data'] = (
                os.path.basename(self._data['sample_data'].name),
                self._data['sample_data'],
                # Mimetyppe is ignored
                'text/plain'
            )

        encoder = MultipartEncoder(fields=fields)

        # NOTE this really should be fixed on the catalogue as well.
        # the way to handle this and deliver an error message more
        # graceful than an arbitary socket closure is for the catalogue
        # to reject the requests with a 'Content-Length' header that's
        # too large.
        if encoder.len > (TEN_MEGABYTES - len(data)):
            raise ValueError(
                f'The sample_data file passed to the'
                ' DatasetBuilder is too large. Please '
                'keep files under 10 megabytes.'
            )

        return encoder

    def with_external_s3_storage(
        self,
        bucket_name,
        aws_account_id,
        prefix
    ):
        """
        Indicate that the dataset will be stored
        in a self-managed S3 bucket outside of the Data Lake.

        :param str bucket_name: Name of the bucket you want to link to this dataset.
        :param str aws_account_id: The AWS account id where this bucket currently resides.
                                   This account needs to be registed on the data lake previously
                                   and your account should have permissions to use it.
        :param str prefix: A valid path that specifies the absolute parent
                           for files in this dataset.
                           This value will be used when issuing access tokens so
                           it is essential that it is as constrained as possible.
                           Cannot end with slash ("/").
        :returns: itself
        :rtype: dli.client.builders.DatasetBuilder

        - **Sample**

        .. code-block:: python

                from dli.client.builders import DatasetBuilder

                builder = DatasetBuilder(
                                package_id="package-id",
                                name="my test dataset",
                                description="My dataset description",
                                content_type="Structured",
                                data_format="CSV",
                                publishing_frequency="Weekly",
                                taxonomy=["Credit", "CDS"]
                                data_preview_type='STATIC',
                                sample_data=open('path/to/my/file.csv')
                        )
                builder = builder.with_external_s3_storage(
                    bucket_name="external-s3-bucket-name",
                    aws_account_id=123456789,
                    prefix="/economic-data-package/my-test-dataset"
                )
                dataset = client.register_dataset(builder)
        """
        self._location_builder = DatasetLocationBuilder().with_external_s3_storage(
            bucket_name=bucket_name,
            aws_account_id=aws_account_id,
            prefix=prefix
        )
        self.payload.update(self._location_builder.build())
        return self

    def with_external_storage(self, location):
        """
        Allows specifying a non S3 location where
        the dataset resides.

        The location will be kept for informational purposes only.

        :param str location: A connection string or identifier where the dataset resides.

        :returns: itself
        :rtype: dli.client.builders.DatasetBuilder

        - **Sample**

        .. code-block:: python

                from dli.client.builders import DatasetBuilder

                builder = DatasetBuilder(
                                package_id="package-id",
                                name="my test dataset",
                                description="My dataset description",
                                content_type="Structured",
                                data_format="CSV",
                                publishing_frequency="Weekly",
                                taxonomy=["Credit", "CDS"]
                        )
                builder = builder.with_external_storage("external-storage-location")
                dataset = client.register_dataset(builder)
        """
        self._location_builder = DatasetLocationBuilder().with_external_storage(location)
        self.payload.update(self._location_builder.build())
        return self

    def build(self):
        return copy.copy(self.payload)

    @staticmethod
    def _validate_preview_type_static(preview_type):
        if preview_type != 'STATIC':
            raise ValueError(
                'Field: data_preview_type must be STATIC when '
                'sample_data is provided'
            )


class DatasetLocationBuilder:
    """
        A simple builder to specify dataset location.
    """

    def __init__(self):
        self.payload = {}

    def with_external_s3_storage(
        self,
        bucket_name,
        aws_account_id,
        prefix
    ):
        """
        Indicate that the dataset will be stored
        in a self-managed S3 bucket outside of the Data Lake.

        :param str bucket_name: Name of the bucket you want to link to this dataset.
        :param str aws_account_id: The AWS account id where this bucket currently resides.
                                   This account needs to be registed on the data lake previously
                                   and your account should have permissions to use it.
        :param str prefix: A vaild path that specifies the absolute parent
                           for files in this dataset.
                           This value will be used when issuing access tokens so
                           it is essential that it is as constrained as possible.
                           Cannot end with slash ("/").

        :returns: itself
        :rtype: dli.client.builders.DatasetLocationBuilder

        - **Sample**

        .. code-block:: python

                from dli.client.builders import DatasetLocationBuilder

                location_builder = DatasetLocationBuilder().with_external_s3_storage(
                        bucket_name="external-s3-bucket-name",
                        aws_account_id=123456789,
                        prefix="/economic-data-package/my-test-dataset"
                    )
                # Build the location object
                location = location_builder.build()
        """
        self.payload["location"] = {
            "type": "S3",
            "owner": {
                "awsAccountId": str(aws_account_id)
            },
            "bucket": bucket_name,
            "prefix": prefix
        }
        return self

    def with_external_storage(self, location):
        """
        Allows specifying a non S3 location where
        the dataset resides.

        The location will be kept for informational purposes only.

        :param str location: A connection string or identifier where the dataset resides.

        :returns: itself
        :rtype: dli.client.builders.DatasetLocationBuilder

        - **Sample**

        .. code-block:: python

                from dli.client.builders import DatasetLocationBuilder

                location_builder = DatasetLocationBuilder().with_external_storage("external-storage-location")
                # Build the location object
                location = location_builder.build()
        """
        self.payload["location"] = {
            "type": "Other",
            "source": location
        }
        return self

    def _dliv2(self):
        """
        The old API used a polymorphic location type.
        The new API uses keys. While more simple we
        have to handle both cases.
        """
        data = {}

        if self.payload['location']['type'] == 'S3':
            data['location'] = {
                's3': copy.copy(self.payload['location'])
            }

            if 'owner' in data['location']['s3']:
                data['location']['s3']['owner']['aws_account_id'] = (
                    # Is camel cased in old API but not new api...
                    data['location']['s3']['owner'].pop('awsAccountId')
                )
        else:
            data['location'] = {
                'other': copy.copy(self.payload['location'])
            }

        return data

    def build(self):
        return copy.copy(self.payload)
