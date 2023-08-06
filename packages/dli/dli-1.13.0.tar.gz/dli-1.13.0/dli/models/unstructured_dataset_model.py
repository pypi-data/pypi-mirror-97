#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import itertools
import logging
import re
from functools import partial
from typing import Optional, List, Union, Tuple

from dli.client.aspects import analytics_decorator, logging_decorator
from dli.models import log_public_functions_calls_using
from dli.models.dataset_model import DatasetModel

trace_logger = logging.getLogger('trace_logger')


class UnstructuredDatasetModel(DatasetModel):

    def __init__(self, **kwargs):

        if "warn" in kwargs:
            warn = kwargs.pop('warn')
            # if warn:
            #     self._client.logger.warning(
            #         "WARN: This is an Unstructured dataset.\n"
            #         "Available methods and method arguments may differ, "
            #         "please see the documentation."
            #     )
        super().__init__(**kwargs, )

    class __DeferInCaseCall(object):
        blurb = """
        Unstructured datasets are different to structured datasets. They have 
        different methods, method arguments and properties.
        You can tell if it is an Unstructured dataset using `ds.content_type` 
        or by `print(ds)`.
        Please see our documentation on using Structured or Unstructured 
        dataset type respectively.
        """

        def __init__(self, name, force_call=False):
            self.name = name
            self.force_call = force_call

        def __repr__(self):
            if self.force_call:
                return self.__call__()
            else:
                raise AttributeError(
                    "This is an Unstructured dataset. There is no such "
                    f"property `{self.name}`.\n{self.blurb}"
                )

        def __call__(self, *args, **kwargs):

            def convert_list(args):
                def formatter(x):
                    if len(x) > 10:
                        return "'" + x[:10] + "...'"
                    else:
                        return "'" + x + "'"

                def joiner(y):
                    return ",".join(list(map(
                        lambda x: x[0] + "=" + formatter(str(x[1])), y.items()
                    )))

                def stringify(x):
                    if type(x) is str:
                        return x
                    elif type(x) is tuple:
                        return ",".join(x)
                    elif type(x) is dict:
                        return joiner(x)
                    else:
                        return str(x)

                return ",".join([stringify(x) for x in args if x])

            raise AttributeError(
                "This is an Unstructured dataset. There is no such method "
                f"`{self.name}({convert_list(args)})`.\n" +
                (f"Method `{self.name}` EXISTS HOWEVER, SO YOU SEEM TO HAVE "
                 "SPECIFIED SOME BAD ARGUMENTS!"
                 if hasattr(UnstructuredDatasetModel, self.name) else "") +
                f"\n{self.blurb}"
            )

    def __getattr__(self, name):

        def wrapper(*args, **kwargs):
            return UnstructuredDatasetModel.__DeferInCaseCall(name)

        return wrapper()

    def __repr__(self):
        return f'<Unstructured Dataset short_code={self.short_code}>'

    def __str__(self):
        return f"UNSTRUCTURED DATASET \"{self.short_code}\""

    def _type_exception_handler(self, exception, func, args, kwargs):
        """
        Needed by aspects.py in order to throw a custom message if the
        function cant be called from it.
        Say, because the arguments are wrong, or the function doesnt exist.
        >N.B. COMMENT THIS OUT IF DEBUGGING!
        """
        if "unexpected" in str(exception):
            UnstructuredDatasetModel.__DeferInCaseCall(func.__name__)(args,
                                                                      kwargs)
        else:
            raise Exception(str(exception))

    def __custom_filter(
        self,
        with_attachments: bool,
        with_metadata: bool,
        with_documents: bool,
        document_types: Optional[Union[str, List[str]]],
        skip_folders_with_zero_matching_documents: bool,
        paths: List[Tuple[str, int]]
    ) -> List[Tuple[str, int]]:
        re_attachments = re.compile("^[^/]+\/[^/]+\/attachment\/.*")
        re_metadata = re.compile("^[^/]+\/[^/]+\/metadata\/.*")
        re_documents = re.compile("^[^/]+\/[^/]+\/document\/.*")

        get_path = lambda x: x[0]

        if not with_attachments:
            paths = filter(
                lambda x: not re_attachments.match(get_path(x)), paths
            )
            trace_logger.info(
                f'Filtering out attachments'
            )

        if not with_metadata:
            paths = filter(
                lambda x: not re_metadata.match(get_path(x)), paths
            )
            trace_logger.info(
                f'Filtering out metadata'
            )

        if not with_documents:
            paths = filter(
                lambda x: not re_documents.match(get_path(x)), paths
            )
            trace_logger.info(
                f'Filtering out documents'
            )
        else:
            paths = list(paths)
            docs = list(filter(
                lambda x: re_documents.match(get_path(x)), paths
            ))
            if len(docs) == 0 and skip_folders_with_zero_matching_documents:
                self._client.logger.warning(
                    'There are no documents in the dataset, so it will not '
                    'be downloaded.'
                    f'\nThere may be metadata or attachments however, repeat '
                    f'the call with '
                    f'`skip_folders_with_zero_matching_documents`=False\n'
                    f'if these are still required.'
                )
                return []

            if document_types:
                paths = filter(
                    lambda x: not re_documents.match(get_path(x)), paths
                )
                if type(document_types) is str:
                    d = [document_types]
                else:
                    d = document_types

                dtypes = '|'.join(d)
                dtypes = dtypes.lower()
                self._client.logger.info(
                    f'Filtering out documents not of type(s): {dtypes}'
                )

                re_filetype = re.compile(f"^(.+/)*(.+).({dtypes})$")
                matching_docs = filter(
                    lambda x: re_filetype.match(get_path(x).lower()), docs)

                paths = list(itertools.chain(paths, matching_docs))

            # TODO need another bit in here to cluster by surviving document_id
            # which still have documents
            if skip_folders_with_zero_matching_documents:
                re_group = re.compile("^[^/]+\/([^/]+)\/document\/.*")
                survivors = []
                doc_ids = "|".join(set(x[0] for x in map(
                    lambda x: re_group.findall(get_path(x)), paths) if x))
                re_survivors = re.compile(f"^[^/]+/({doc_ids})/[^/]*/.*")
                paths = list(
                    filter(lambda x: re_survivors.match(get_path(x)), paths))

        return list(paths)

    def __common_download(self, destination_path, **kwargs):
        return self._DatasetModel__download(
            destination_path=destination_path,
            flatten=False,
            custom_filter_func=partial(
                self.__custom_filter, **kwargs
            ),
            # we dont know if there are hidden yet.
            # may need to set to True
            skip_hidden_files=False
        )

    def list(
        self,
        request_id=None,
        absolute_path: bool = True,
        skip_hidden_files: bool = False,
    ) -> List[str]:
        """
        List all the paths to files in the dataset. Calls go via the
        Datalake's S3 proxy, so the returned paths will be returned
        in the
        style of the S3 proxy, so in the pattern
        `s3://organisation_short_code/dataset_short_code/<path>`.
        S3 proxy does not return direct paths to the real location
        on S3 as
        they may be sensitive.

        The list will filter out paths where:
        * The size is zero bytes.
        * The name of any partition within the path is prefixed with
        a `.` or
        a `_` as that means it is intended as a hidden file.
        * The name of any partition within the path is exactly the word
        `metadata`.
        * It is a directory rather than a file.
        * Files with the wrong extension for the dataset's type i.e for
        a .parquet dataset we will return only .parquet files,
        zero .csv
        files.

        Parameters
        ----------
        :param str request_id: Optional. Automatically generated value
            used by our logs to correlate a user journey across several
            requests and across multiple services.

        :param bool absolute_path: True (default) for returning an
            absolute path to the path on the S3 proxy. False to
            return a
            relative path (this is useful if using a TransferManager).

        :param bool skip_hidden_files: True (default) skips files
        that have
            been uploaded to S3 by Spark jobs. These usually start
            with a
            `.` or `_`.
        """
        return self._DatasetModel__list(
            request_id=request_id,
            custom_filter_func=None,
            absolute_path=absolute_path,
            skip_hidden_files=skip_hidden_files
            # n.b. We need to decide if you can list by filtering
            # with_attachments, with_metadata, doc_types too
        )

    def download(
        self,
        destination_path: str,
        with_attachments: bool = True,
        with_metadata: bool = True,
        document_types: Optional[Union[str, List[str]]] = None,
        skip_folders_with_zero_matching_documents: bool = True
    ) -> List[str]:
        """
        Downloads the original unstructured dataset files from the data lake
        to local copy, to a destination of your choice.

        If the dataset does not have any document_id's within it a message
        will be shown stating this.

        If the filters do match any of the document_id's in the dataset such
        that no document_id will be downloaded
        (as skip_folders_with_zero_matching_documents=True), a message
        stating the filter does not match any documents with be shown
        stating this.

        For example:

        .. code-block:: python

            import dli
            client = dli.connect()
            dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
            # Download all the files in this dataset to the specified
            # directory.
            dataset.download('C:\\tmp') # Path for Windows temp directory.

        :example:
            /document_id=233/
                /attachments/      --> @see with_attachments
                   file.pdf
                   file2.xml
                /document/
                    file.html      --> downloaded
                    ...
                /metadata/         --> @see with_metadata
                    ...

        Parameters
        ----------
        :param str destination_path: required. The path on the system,
            where the files should be saved. Must be a directory, if does not
            exist, will be created.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                dataset.download('C:\\tmp') # Path for Windows temp directory.

            :example:

                /document_id=233/
                    /attachments/      --> downloaded only when "with_attachments" is set to True
                       file.pdf
                       file2.xml
                    /document/
                        file.html      --> downloaded
                        ...
                    /metadata/         --> @see with_metadata
                        ...

        :param bool with_attachments:
            An unstructured dataset comprises of one of more document folder
            prefixes e.g. {document_id=233, document_id=132}
            Specifies whether to download the attachments folder prefix within
            each document_id prefix. Default is True.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                # Download everything except the attachments directory.
                dataset.download(
                    'C:\\tmp',
                     with_attachments=False
                )

            :example:
                "with_attachments" is set to False

                /document_id=233/
                    /document/
                        file.html      --> downloaded
                        ...
                    /metadata/         --> @see with_metadata
                        ...

            :example:
                "with_attachments" is set to True

                /document_id=233/
                    /attachments/      --> downloaded only when "with_attachments" is set to True
                       file.pdf
                       file2.xml
                    /document/
                        file.html      --> downloaded
                        ...
                    /metadata/         --> @see with_metadata
                        ...

        :param bool with_metadata:
            An unstructured dataset comprises of one of more document folder
            prefixes e.g. {document_id=233, document_id=132}
            Specifies whether to download the metadata folder prefix within
            each document_id prefix. Default is True.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                # Download everything except the metadata directory.
                dataset.download(
                    'C:\\tmp',
                    with_metadata=False
                )

            :example:
                "with_metadata" is set to False

                /document_id=233/
                    /attachments/      --> @see with_attachments
                       ...
                    /document/
                        file.html      --> downloaded
                        ...

            :example:
                "with_metadata" is set to True

                /document_id=233/
                    /attachments/      --> @see with_attachments
                       ...
                    /document/
                        file.html      --> downloaded
                        ...
                    /metadata/         --> download only when "with_metadata" is set to True
                        summary.json

        :param str document_types: Optional[Union[str, List[str]]].
            A string or a list of strings representing the desired file types
            to download.
            Filter the documents in the /document/ folder prefix of each
            document_id in the dataset
            according to the file's prefix. Default is None.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                # Download everything that is a document with file type "html".
                # This will not filter inside the attachments or metadata
                # directories.
                document_types = ["html"]
                dataset.download(
                    'C:\\tmp',
                    document_types=document_types
                )

            :example:
                document_types is set to ["html"] or "html"

                /document_id=233/
                    /attachments/
                       file.pdf
                       ...
                    /document/
                        file.html      --> downloaded
                        file2.pdf      --> not downloaded
                        file3.xml      --> not downloaded
                        ...
                    /metadata/
                        summary.json
                        ...

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                # Download everything that is a document with file type "pdf"
                # or "xml".
                # This will not filter inside the attachments or metadata
                # directories.
                document_types = ["pdf", "xml"]
                dataset.download(
                    'C:\\tmp',
                    document_types=document_types
                )

            :example:
                document_types is set to ["pdf", "xml"]

                /document_id=233/
                    /attachments/
                       file.pdf
                       ...
                    /document/
                        file.html      --> not downloaded
                        file2.pdf      --> downloaded
                        file3.xml      --> downloaded
                        ...
                    /metadata/
                        summary.json
                        ...

        :param bool skip_folders_with_zero_matching_documents:
            After applying document_types the document_id's /document/ folder
            may be empty,
            since the file types may not match the chosen types.
            The document_id's without any post-filter documents are filtered
            out by default to minimize
            download and retain only the folders bearing document_id's that
            matched the filter.

            It may be wished to download the document_id regardless of the
            folder being empty if the metadata or
            attachments are needed despite an empty /document/ folder. This
            is achieved by setting the value to False.
            Default is True.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                # Download everything that is a document with file type "pdf"
                # or "xml".
                # This will not filter inside the attachments or metadata
                # directories.
                document_types = ["xml"]
                dataset.download(
                    'C:\\tmp',
                    document_types=document_types,
                    skip_folders_with_zero_matching_documents=True
                )

            :example:
                when document_types = ["xml"] and skip_folders_with_zero_matching_documents = True

                /document_id=233/     --> not downloaded as /document/ empty
                after filter
                    /attachments/
                       file.pdf
                       ...
                    /document/      --> not downloaded
                        file.html      --> not downloaded
                        file2.pdf      --> not downloaded
                        ...
                    /metadata/
                        summary.json
                        ...

            :example:
                when document_types = ["xml"] and skip_folders_with_zero_matching_documents = False

                /document_id=233/      --> downloaded despite /document/ being empty after filter
                    /attachments/
                       file.pdf
                    /metadata/
                        summary.json
        """

        return self.__common_download(
            destination_path,
            with_attachments=with_attachments,
            with_metadata=with_metadata,
            with_documents=True,
            document_types=document_types,
            skip_folders_with_zero_matching_documents=skip_folders_with_zero_matching_documents
        )

    def download_metadata(self, destination_path: str) -> List[str]:
        """
        Helper function to call `download` with the settings to only download
        files that are in the /metadata directory.

        :param str destination_path: required. The path on the system,
            where the files should be saved. Must be a directory, if does not
            exist, will be created.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                dataset.download('C:\\tmp') # Path for Windows temp directory.

            :example:

                /document_id=233/
                    /attachments/      --> downloaded only when "with_attachments" is set to True
                       file.pdf
                       file2.xml
                    /document/
                        file.html      --> downloaded
                        ...
                    /metadata/         --> @see with_metadata
                        ...
        :return: List[str]
        """

        return self.__common_download(
            destination_path=destination_path,
            with_attachments=False,
            with_metadata=True,
            with_documents=False,
            document_types=None,
            skip_folders_with_zero_matching_documents=False
        )

    def download_attachments(self, destination_path: str) -> List[str]:
        """
        Helper function to call `download` with the settings to only download
        files that are in the /attachments directory.

        :param str destination_path: required. The path on the system,
            where the files should be saved. Must be a directory, if does not
            exist, will be created.

            .. code-block:: python

                import dli
                client = dli.connect()
                dataset = client.datasets.get(<dataset shortcode>, Optional:<organisation_short_code>)
                dataset.download('C:\\tmp') # Path for Windows temp directory.

            :example:

                /document_id=233/
                    /attachments/      --> downloaded only when "with_attachments" is set to True
                       file.pdf
                       file2.xml
                    /document/
                        file.html      --> downloaded
                        ...
                    /metadata/         --> @see with_metadata
                        ...
        :return: List[str]
        """

        return self.__common_download(
            destination_path=destination_path,
            with_attachments=True,
            with_metadata=False,
            with_documents=False,
            document_types=None,
            skip_folders_with_zero_matching_documents=False
        )


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['dataset_id']
)(UnstructuredDatasetModel)
