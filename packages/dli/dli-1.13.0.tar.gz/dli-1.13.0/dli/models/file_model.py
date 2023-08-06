#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import contextlib
import os
import shutil
import ntpath
from typing import Generator
from io import BufferedReader
from urllib.parse import urljoin, urlparse

from dli.client.aspects import analytics_decorator, logging_decorator
from dli.client.components.urls import consumption_urls
from dli.models import log_public_functions_calls_using, AttributesDict


def flatten_s3_file_path(s3_path):
    path = urlparse(s3_path)[2]  # [scheme, netloc, path, ...]
    head, tail = ntpath.split(path)
    file = tail or ntpath.basename(head)
    return file


def get_or_create_os_path(s3_path: str, to: str, flatten: bool) -> str:
    if flatten:
        destination_key = flatten_s3_file_path(s3_path)
    else:
        destination_key = urlparse(s3_path).path.lstrip('/')

    to_path = os.path.join(
        to, os.path.normpath(destination_key)
    )

    to_path = os.path.abspath(to_path)

    if len(to_path) > 259 and os.name == 'nt':
        raise Exception(f"Apologies {s3_path} can't be downloaded "
                        f"as the file name would be too long. You "
                        f"may want to try calling again with "
                        f"Instance.download(flatten=True), which "
                        f"will put the file in a directory of your choice")

    else:
        directory, _ = os.path.split(to_path)
        os.makedirs(directory, exist_ok=True)

    return to_path


class FileModel(AttributesDict):

    @contextlib.contextmanager
    def open(self) -> Generator[BufferedReader, None, None]:
        """
        Context manager that yields a file like object.

        :example:
            
            .. code-block::

                with file.open() as f:
                    print(f.read())
                    
        
        .. note::
            
            The return type is a BufferedReader. This is the
            raw HTTP stream. This means that unlike usual file
            objects you can no seek it, it can only be read
            in order. So save to a file or buffer if you wish
            to manipulate the file out of order.

        """
        response = self._client.session.get(
            urljoin(
                self._client._environment.consumption,
                consumption_urls.consumption_download.format(
                    id=self.datafile_id,
                    path=self.path
                )
            ),
            stream=True
        )
        # otherwise you get raw secure
        response.raw.decode_content = True
        yield response.raw
        response.close()

    def download(self, to='./', flatten=False) -> str:
        """
        Download the files for the instance, then return a list of the file
        paths that were written.

        :param str to: The path on the system, where the files
            should be saved. must be a directory, if doesn't exist, will be
            created.

        :param bool flatten: The default behaviour (=False) is to use the s3
            file structure when writing the downloaded files to disk.
            When flatten = True, we remove the s3 structure.

        :return: Directory to path of the downloaded files.

        :example:

            Downloading without flatten:

            .. code-block:: python

                >>> dataset.instances.lastest().files()[0].download('./local/path/')
                './local/path/as_of_date=2019-09-10/type=full/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',


        :example:

            When flatten = True, we remove the s3 structure. Example:

            Example output for new behaviour:

            .. code-block:: python

                >>> dataset.instances.lastest().files()[0].download('./local/path/', flatten=True)
                './local/path/StormEvents_details-ftp_v1.0_d1950_c20170120.csv.gz',

        """
        to_path = get_or_create_os_path(
            s3_path=self.path, to=to, flatten=flatten
        )

        print(f'Downloading {self.path} to: {to_path}...')

        with self.open() as download_stream:
            with open(to_path, 'wb') as target_download:
                # copyfileobj is just a simple buffered
                # file copy function with some sane
                # defaults and optimisations.
                shutil.copyfileobj(
                    download_stream, target_download
                )
                print(f'Completed download to: {to_path}.')

        return to_path


log_public_functions_calls_using(
    [analytics_decorator, logging_decorator],
    class_fields_to_log=['datafile_id', 'path']
)(FileModel)
