import io
import json
import os
import random
import re
import tempfile
from contextlib import redirect_stdout
from functools import partial
from unittest.mock import MagicMock, call

import jwt
import numpy
import pandas
import pyarrow
import pytest

from dli.client.exceptions import DataframeStreamingException, TimeoutException
from pyarrow.lib import ArrowInvalid
from tests.models.conftest import mock_catalogue_filter_search_response_impl


@pytest.fixture
def instance_file(client):
    client._environment.consumption = 'consumption-test.local'

    instance = client._Instance(
        datafile_id='123',
        total_size=1048576
    )

    client._session.get().json.return_value = {
        'data': [{
            'attributes': {
                'path': 'prefix/test.001.csv',
                'metadata': {}
            }
        }]
    }

    files = instance.files()
    file_ = files[0]

    client.session.reset_mock()

    client._session.get().raw.read.side_effect = [
        b'hello world',
        b''
    ]

    yield file_


class TestDataset:

    @pytest.fixture
    def dataset_load_type_none(self, client):
        return client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Structured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

    @pytest.fixture
    def dataset_load_type_incremental(self, client):
        return client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Structured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                    'load_type': 'Incremental Load',
                }
            }
        })

    @pytest.fixture
    def dataset_load_type_full(self, client):
        return client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Structured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                    'load_type': 'Full Load',
                }
            }
        })

    def __setup_mocks(
        self,
        monkeypatch,
        filter_returns_all_prefixes: bool = False,
        has_filter_path_2020: bool = False,
        skip_hidden_files: bool = True,
    ):
        # This has a directory name starting with `.` so must be ignored.
        self.key_latest_0 = MagicMock()
        self.key_latest_0.key = 'abc/.latest/country=fr/' \
                                'nulls_and_unicode.parquet'
        self.key_latest_0.size = 1

        # This has a directory name `as_of=latest` so must be ignored.
        self.key_latest_1 = MagicMock()
        self.key_latest_1.key = 'abc/as_of_date=latest/country=fr/' \
                                'nulls_and_unicode.parquet'
        self.key_latest_1.size = 1

        # This older as_of must be ignored for a full type.
        self.key_2019_0 = MagicMock()
        self.key_2019_0.key = 'abc/as_of_date=2019/country=uk/' \
                              'alltypes_dictionary.parquet'
        self.key_2019_0.size = 1

        self.key_2019_1 = MagicMock()
        self.key_2019_1.key = 'abc/as_of_date=2019/country=us/' \
                              'alltypes_plain.parquet'
        self.key_2019_1.size = 1

        self.key_2020_0 = MagicMock()
        # Note: a key is a relative path starting after the s3://bucket/prefix
        # for this dataset.
        self.key_2020_0.key = 'abc/as_of_date=2020/country=uk/' \
                              'avro.parquet'
        self.key_2020_0.size = 1
        self.key_2020_1 = MagicMock()
        self.key_2020_1.key = 'abc/as_of_date=2020/country=us/' \
                              'nulls_and_unicode.parquet'
        self.key_2020_1.size = 1

        self.filter_mock = MagicMock()

        prefix_2020 = [self.key_2020_0, self.key_2020_1]

        if skip_hidden_files and filter_returns_all_prefixes:
            _filter_side_effects = iter([
                # All files when listing.
                [
                    self.key_2019_0, self.key_2019_1, self.key_2020_0,
                    self.key_2020_1
                ]
            ])
        elif not skip_hidden_files and filter_returns_all_prefixes:
            _filter_side_effects = iter([
                # All files when listing.
                [
                    self.key_latest_0, self.key_latest_1, self.key_2019_0,
                    self.key_2019_1, self.key_2020_0, self.key_2020_1
                ]
            ])
        else:
            _filter_side_effects = iter([
                # All files when listing.
                prefix_2020
            ])

        self.filter_mock.side_effect = _filter_side_effects

        self.objects_mock = MagicMock()
        self.objects_mock.return_value.filter = self.filter_mock

        self.bucket_mock = MagicMock()
        self.bucket_mock.return_value.objects = self.objects_mock()

        self.resource_mock = MagicMock()
        self.resource_mock.return_value.Bucket = self.bucket_mock

        if has_filter_path_2020:
            _common_prefixes = {
                'CommonPrefixes': [
                    {'Prefix': 'abc/as_of_date=2020/'}
                ]
            }
        else:
            _common_prefixes = {
                'CommonPrefixes': [
                    {'Prefix': 'abc/.latest/'},
                    {'Prefix': 'abc/as_of_date=latest/'},
                    {'Prefix': 'abc/as_of_date=2019/'},
                    {'Prefix': 'abc/as_of_date=2020/'},
                ]
            }
        self.resource_mock.return_value.meta.client.list_objects_v2.\
            return_value = _common_prefixes

        self.boto_mock = MagicMock()
        self.boto_mock.return_value.resource.return_value = \
            self.resource_mock()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            self.boto_mock
        )

    def test_dataset_partitions_zero_partitions(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        """
        Edge case where the S3 structure does not have an partitions.

        :param monkeypatch:
        :return:
        """
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=True)

        key_zero_partitions = MagicMock()
        key_zero_partitions.key = 'abc/one/two/alltypes_dictionary.parquet'
        key_zero_partitions.size = 1

        _filter_side_effects = iter([
            [key_zero_partitions]
        ])

        self.filter_mock.side_effect = _filter_side_effects

        partitions = dataset_load_type_incremental.partitions()

        assert partitions == {}

    def test_dataset_partitions_load_type_incremental(
        self,
        dataset_load_type_incremental,
        monkeypatch
    ):
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=True)

        partitions = dataset_load_type_incremental.partitions()

        assert partitions == {
            'as_of_date': ['2019', '2020'],
            # Note: we must not get any partitions from the hidden folders.
            'country': ['uk', 'us'],
        }

    def test_dataset_partitions_load_type_full(
        self,
        dataset_load_type_full,
        monkeypatch
    ):
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=False)

        partitions = dataset_load_type_full.partitions()

        assert partitions == {
            'as_of_date': ['2020'],
            'country': ['uk', 'us'],
        }

    def test_dataset_instances_is_iterable(self, dataset_load_type_none):
        datafiles = dataset_load_type_none.instances.all()
        assert hasattr(datafiles, '__iter__')

    def test_dataset_download_refers_to_latest_instance(
        self,
        dataset_load_type_incremental,
    ):
        path = './destination_path'

        dataset_load_type_incremental.instances.latest = MagicMock(
            download=MagicMock(return_value='file')
        )

        result = dataset_load_type_incremental.instances.latest.download(path)

        dataset_load_type_incremental.instances.latest.download.\
            assert_called_once_with(path)

        assert result == 'file'

    def test_dataset_instances_make_requests_on_iteration(
        self,
        client,
        dataset_load_type_incremental,
    ):
        client._session.get().json.side_effect = [
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 1}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 2}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 3}
                }]
            },
        ]

        instances = list(dataset_load_type_incremental.instances.all())
        assert len(instances) == 3

    def test_dataset_instances_make_multiple_iterations(
        self,
        client,
        dataset_load_type_incremental,
    ):
        client._session.get().json.side_effect = [
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 1}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 2}
                }]
            },
            {
                'properties': {'pages_count': 3},
                'entities': [{
                    'properties': {'datasetId': 3}
                }]
            },
        ]

        def mock_iter():
            if not hasattr(mock_iter, 'call_count'):
                mock_iter.call_count = 0
                mock_iter.cached = False

            if not mock_iter.cached:
                mock_iter.call_count += 1
                mock_iter.cached = True

            yield from [1, 2, 3]

        instances = list(dataset_load_type_incremental.instances.all())

        assert len(instances) == 3

        instances_from_cache = list(
            dataset_load_type_incremental.instances.all()
        )

        assert len(dataset_load_type_incremental.instances._paginator.cache) \
               == 3
        assert len(instances_from_cache) == 3

    def test_dataset_download_plain(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(monkeypatch)

        with tempfile.TemporaryDirectory() as target_dest:
            dataset_load_type_incremental.download(target_dest)

        self.boto_mock.assert_called()
        self.resource_mock.assert_called_once()
        self.bucket_mock.assert_has_calls([
            call('abc')
        ])
        self.objects_mock.assert_called_once()
        self.filter_mock.assert_has_calls([
            # Assert that we only call the non-hidden prefixes.
            call(Prefix='abc/as_of_date'),
        ], any_order=True)

    def test_dataset_download_filter_prefix(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(monkeypatch, has_filter_path_2020=True)

        with tempfile.TemporaryDirectory() as target_dest:
            dataset_load_type_incremental.download(
                target_dest,
                filter_path='as_of_date=2020',
            )

        assert (
            self.boto_mock().resource().Bucket()
            .objects.filter.call_args[1]['Prefix']
        ) == 'abc/as_of_date=2020'

    # TODO
    # def test_dataset_is_wrapped_with_analytics_logger(self, client,
    #                                                   monkeypatch,
    #                                                   instance_file):
    #     boto_mock = MagicMock()
    #     monkeypatch.setattr('dli.aws.Session', boto_mock)
    #
    #     dataset = client._DatasetFactory._from_v2_response({
    #         'data': {
    #             'id': '1234',
    #             'attributes': {
    #                 'content_type': 'Structured',
    #                 'location': {},
    #                 'organisation_short_code': 'abc',
    #                 'short_code': 'abc',
    #                 'has_access': True,
    #             }
    #         }
    #     })
    #
    #     with tempfile.TemporaryDirectory() as target_dest:
    #         dataset.download(target_dest)
    #
    #     client._analytics_handler.create_event.call_count = 2
    #     client._analytics_handler.create_event.assert_any_call(
    #         # Not testing the extract user metadata here
    #         ANY, ANY,
    #         'DatasetModel',
    #         '_DatasetModel__download',
    #         {
    #             'self': dataset,
    #             'destination_path': target_dest,
    #             'dataset_id': '1234'
    #         },
    #         result_status_code=200
    #     )

    def test_dataset_info(self, test_client, dataset_request_v2,
                          dictionary_request_v2, fields_request_v2):
        test_client.session.reset_mock()
        test_client._session.get.return_value.json.side_effect = [
            dictionary_request_v2, fields_request_v2
        ]

        dataset = test_client._DatasetFactory._from_v2_response(
            dataset_request_v2
        )

        def redirect(fun):
            with io.StringIO() as buf, redirect_stdout(buf):
                fun()
                output = buf.getvalue()
                return output

        assert(
            redirect(dataset.info)
            .replace(" ", "").replace("\n", "")
            ==
            """
                name    type
                ------  -----------------
                col1    String (Nullable)
                col2    String (Nullable)
                col3    String
            """
            .replace(" ", "").replace("\n", "")
        )

    def test_dataset_list_load_type_none(
        self,
        monkeypatch,
        dataset_load_type_none,
    ):
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=True)

        ls = dataset_load_type_none.list()

        self.boto_mock.assert_called_once()
        self.resource_mock.assert_called_once()
        self.bucket_mock.assert_has_calls([
            call('abc')
        ])
        self.objects_mock.assert_called_once()
        self.filter_mock.assert_has_calls([
            # Assert that we only call the non-hidden prefixes.
            call(Prefix='abc/as_of_date'),
        ], any_order=True)

        assert all(type(elem) is str for elem in ls)
        assert ls == [
            # Note: the path is now an absolute path in the format:
            # s3://bucket/prefix/key
            f's3://abc/{self.key_2019_0.key}',
            f's3://abc/{self.key_2019_1.key}',
            f's3://abc/{self.key_2020_0.key}',
            f's3://abc/{self.key_2020_1.key}',
        ], f'Unexpected keys in list: {ls}'

    def test_dataset_list_load_type_incremental(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=True)

        ls = dataset_load_type_incremental.list()

        self.boto_mock.assert_called_once()
        self.resource_mock.assert_called_once()
        self.bucket_mock.assert_has_calls([
            call('abc')
        ])
        self.objects_mock.assert_called_once()
        self.filter_mock.assert_has_calls([
            # Assert that we only call the non-hidden prefixes.
            call(Prefix='abc/as_of_date'),
        ], any_order=True)

        assert all(type(elem) is str for elem in ls)
        assert ls == [
            # Note: the path is now an absolute path in the format:
            # s3://bucket/prefix/key
            f's3://abc/{self.key_2019_0.key}',
            f's3://abc/{self.key_2019_1.key}',
            f's3://abc/{self.key_2020_0.key}',
            f's3://abc/{self.key_2020_1.key}',
        ], f'Unexpected keys in list: {ls}'

    def test_dataset_list_load_type_full(
        self,
        monkeypatch,
        dataset_load_type_full,
    ):
        self.__setup_mocks(
            monkeypatch,
            # Full Load will only list paths under the most recent `as_of_`
            # common prefix, so it will never see paths from outside that
            # common prefix.
            filter_returns_all_prefixes=False,
        )

        ls = dataset_load_type_full.list()

        self.boto_mock.assert_called_once()
        self.resource_mock.assert_called_once()
        self.bucket_mock.assert_has_calls([
            call('abc')
        ])
        self.objects_mock.assert_called_once()
        self.filter_mock.assert_has_calls([
            # Assert that we only call the most recent common prefix.
            call(Prefix='abc/as_of_date=2020/'),
        ])

        assert all(type(elem) is str for elem in ls)
        assert ls == [
            # Note: the path is now an absolute path in the format:
            # s3://bucket/prefix/key
            f's3://abc/{self.key_2020_0.key}',
            f's3://abc/{self.key_2020_1.key}',
        ], "Expected load type 'Full Load' to have one as_of partition " \
           f"with two files, but list was '{ls}'"

    def test_dataset_list_partition_filter(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=True)

        ls = dataset_load_type_incremental.list(partitions="as_of_date=2020")

        assert len(ls) == 2

    def test_dataset_list_partition_filter_load_type_full_for_wrong_partition(
        self,
        monkeypatch,
        dataset_load_type_full
    ):
        self.__setup_mocks(monkeypatch, filter_returns_all_prefixes=False)

        ls = dataset_load_type_full.list(partitions="as_of_date=2019")

        assert len(ls) == 0, 'Expected empty list because this as_of_ will' \
                             f'not be inside the full load, but got list: {ls}'

    def test_dataset_list_filter_path(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(
            monkeypatch,
            filter_returns_all_prefixes=False,
            has_filter_path_2020=True,
        )

        ls = dataset_load_type_incremental.list(filter_path="as_of_date=2020")

        assert len(ls) == 2

    def test_dataset_list_absolutely(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(monkeypatch)

        ls = dataset_load_type_incremental.list(absolute_path=True)

        assert all(map(lambda x: x.startswith("s3://"), ls)), f'List: {ls}'

    def test_dataset_list_relatively(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(monkeypatch)

        ls = dataset_load_type_incremental.list(absolute_path=False)

        assert all(map(lambda x: not x.startswith("s3://"), ls)), f'List: {ls}'

    def test_dataset_list_not_skipping_hidden_files(
        self,
        monkeypatch,
        dataset_load_type_incremental,
    ):
        self.__setup_mocks(
            monkeypatch,
            filter_returns_all_prefixes=True,
            skip_hidden_files=False,
        )

        ls = dataset_load_type_incremental.list(skip_hidden_files=False)

        assert len(ls) == 6, 'Expected two from .latest, two from 2020 and ' \
                             f'two from 2020, but got list: {ls}'

    def test_dataset_list_intersecting_partition_and_path(
        self,
        dataset_load_type_incremental,
    ):
        with pytest.raises(ValueError) as excinfo:
            dataset_load_type_incremental.list(
                filter_path="some-filter_path",
                partitions='some-partition',
            )

        message = 'Both `partitions` and `filter_path` are set. Please only ' \
            'provide one of these parameters.'
        assert message in str(excinfo.value)

    def test_dataset_download_intersecting_partition_and_path(
        self,
        dataset_load_type_incremental,
    ):

        with pytest.raises(ValueError) as excinfo:
            dataset_load_type_incremental.download(
                destination_path='.',
                filter_path="some-filter_path",
                partitions=['some-partition'],
            )

        message = 'Both `partitions` and `filter_path` are set. Please only ' \
            'provide one of these parameters.'
        assert message in str(excinfo.value)


class TestFileDownload:

    def test_instance_file_download_simple(self, instance_file):
        old_dir = os.path.abspath(os.curdir)

        with tempfile.TemporaryDirectory() as target_dest:
            os.chdir(os.path.abspath(target_dest))
            instance_file.download()
            with open(os.path.join(target_dest, 'prefix/test.001.csv')) as f:
                assert f.read() == 'hello world'

        os.chdir(old_dir)

    def test_instance_file_download_with_path(self, instance_file):
        with tempfile.TemporaryDirectory() as target_dest:
            instance_file.download(target_dest)
            with open(os.path.join(target_dest, 'prefix/test.001.csv')) as f:
                assert f.read() == 'hello world'

    def test_instance_file_download_non_existent_path(
        self, instance_file
    ):
        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a/b/c/')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'hello world'

    def test_instance_file_download_non_existent_file(
        self, instance_file
    ):
        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'hello world'

    def test_instance_file_overwrites(
        self, client, instance_file
    ):
        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'hello world'

        client.session.reset_mock()
        client._session.get().raw.read.side_effect = [
            b'brave new world',
            b''
        ]

        with tempfile.TemporaryDirectory() as target_dest:
            target_dest = os.path.join(target_dest, 'a')
            instance_file.download(target_dest)
            with open(os.path.join(
                target_dest, 'prefix/test.001.csv'
            )) as f:
                assert f.read() == 'brave new world'


class TestInstanceDownload:

    @pytest.fixture
    def instance(self, client):
        client._environment.consumption = 'consumption-test.local'

        instance = client._Instance(
            datafile_id='123'
        )

        client._session.get().json.return_value = {
            'data': [{
                'attributes': {
                    'path': f's3://bucket/prefix/test.00{i}.csv',
                    'metadata': {}
                }
            } for i in range(3)
            ]
        }

        yield instance

    def test_instance_download_all_should_refer_to_download_function(
        self,
        instance
    ):
        path = './target'
        instance.download = MagicMock(return_value='file')
        result = instance.download_all(path, flatten=False)

        instance.download.assert_called_once_with(path, False)
        assert result == 'file'

    def test_instance_download_flatten(self, client, instance):
        client._session.get().raw = io.BytesIO(b'abc')

        with tempfile.TemporaryDirectory() as target_dest:
            to = os.path.join(target_dest, 'a')
            result = instance.download_all(to, flatten=True)
            directory_of_flattened = result[0].split('/test')[0]
            list_dir = sorted(os.listdir(directory_of_flattened))

            assert (
                list_dir ==
                ['test.000.csv', 'test.001.csv', 'test.002.csv']
            )


class TestInstanceDataframe:

    @pytest.fixture
    def arrow_ipc_stream(self) -> (pandas.DataFrame, io.BytesIO):
        # Rows:
        # 100 -> 205.5 kB (205,548 bytes) on disk in 0.44 seconds.
        # 10000 -> 9.2 MB (9,234,131 bytes) on disk in 0.67 seconds.

        max_rows = 10000
        # Max columns should match a worst case. For Transaction Analysis
        # there are over 369 columns.
        max_columns = 372

        num_column_types = 6

        # Seed the random number generator so that we can reproduce the output.
        numpy.random.seed(0)

        def bools_df():
            return pandas.DataFrame(
                numpy.random.choice(
                    [False, True],
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_bool_{x}') for x in
                         range(int(max_columns / num_column_types))],
                dtype='bool',
            )

        def ints_df():
            return pandas.DataFrame(
                numpy.random.randint(
                    low=0,
                    high=1000000,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_int_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def floats_df():
            return pandas.DataFrame(
                numpy.random.rand(
                    max_rows,
                    int(max_columns / num_column_types)),
                columns=[str(f'column_float_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def string_df():
            import pandas.util.testing
            return pandas.DataFrame(
                numpy.random.choice(
                    pandas.util.testing.RANDS_CHARS,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_str_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def dates_df():
            dates = pandas.date_range(start='1970-01-01', end='2020-01-01')

            return pandas.DataFrame(
                numpy.random.choice(
                    dates,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_date_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        def datetimes_df():
            datetimes = pandas.date_range(start='1970-01-01', end='2020-01-01',
                                          freq='H')

            return pandas.DataFrame(
                numpy.random.choice(
                    datetimes,
                    size=(max_rows, int(max_columns / num_column_types))
                ),
                columns=[str(f'column_datetime_{x}') for x in
                         range(int(max_columns / num_column_types))],
            )

        df = pandas.concat(
            [
                bools_df(),
                datetimes_df(),
                ints_df(), floats_df(), string_df(), dates_df(),
            ],
            # Concat columns axis
            axis=1,
            copy=False
        )

        # Randomise the column order so the compression cannot optimise
        # easily based on types as this will mix float columns among the int
        # columns.
        random_column_order = df.columns.tolist()
        random.shuffle(random_column_order)
        df = df[random_column_order]

        assert df.shape[0] == max_rows
        assert df.shape[1] == max_columns

        sink = pyarrow.BufferOutputStream()
        batch = pyarrow.RecordBatch.from_pandas(df=df, nthreads=1)
        writer = pyarrow.RecordBatchStreamWriter(sink, batch.schema)
        writer.write_batch(batch)
        # It's important the IPC stream is closed
        writer.close()
        var = sink.getvalue()
        return df, io.BytesIO(var)

    @pytest.fixture
    def dataset(self, client):
        return client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Structured',
                    'location': {},
                    'has_access': True,
                    'short_code': 'some-short-code',
                }
            }
        })

    def test_dataset_dataframe(self, benchmark, arrow_ipc_stream,
                               dataset):

        test_dataframe, stream = arrow_ipc_stream
        dataset._client = MagicMock()
        dataset._client._environment.consumption = 'https://test/'
        dataset._client.session.get().status_code = 200
        msg = json.dumps({
            'status': 200,
        }).encode('utf')

        _io_bytesio_seekend = 2
        stream.seek(0, _io_bytesio_seekend)
        stream.write(msg)

        def _bench():
            stream.seek(0)
            # reset our fake socket
            dataset._client.session.get().raw = stream
            return dataset.dataframe()

        # The benchmark code will run several times to get an average runtime.
        df = benchmark(_bench)

        # Check that we can read from the file that was written.
        pandas.testing.assert_frame_equal(test_dataframe, df)

    def test_dataframe_handle_errors(self, arrow_ipc_stream,
                                     dataset):
        test_dataframe, stream = arrow_ipc_stream
        error_msg = json.dumps({
            'status': 400,
        }).encode('utf')

        _io_bytesio_seekend = 2
        stream.seek(0, _io_bytesio_seekend)
        stream.write(error_msg)
        stream.seek(0)

        dataset._client = MagicMock()
        dataset._client._environment.consumption = 'https://test/'

        dataset._client.session.get().raw = stream
        dataset._client.session.get().status_code = 200

        with pytest.raises(DataframeStreamingException):
            dataset.dataframe(1)

    def test_dataframe_handle_arrowinvalid_exception(
            self, arrow_ipc_stream, dataset
    ):
        arrow_ipc_stream = io.BytesIO(b'invalid')

        arrow_ipc_stream.seek(0)

        dataset._client = MagicMock()
        dataset._client._environment.consumption = 'https://test/'

        dataset._client.session.get().raw = arrow_ipc_stream
        dataset._client.session.get().status_code = 200

        with pytest.raises(ArrowInvalid) as excinfo:
            dataset.dataframe(1)

        message = r'Sorry, the dataframe you are trying to read is too ' \
                  'large to fit into memory. Please consider one of these ' \
                  'alternatives:' \
                  '\n\n1. Run the same code on a machine that has more ' \
                  'RAM, for example a Jupyter Notebook hosted on an AWS ' \
                  'environment.'\
                  '\n2. Use a big data tool such as Spark, Dask or similar ' \
                  'to read the data via our S3 proxy. Unlike Pandas, these ' \
                  'big data tools are able to apply some operations such ' \
                  'as filtering without having to hold all of the data ' \
                  'into memory. See https://supportlibrary.ihsmarkit.com/' \
                  'display/DLSL/Using+the+S3+Proxy+with+Big+Data+tooling' \
                  '\n\nOriginal exception: '

        error_message = str(excinfo.value)
        assert error_message.startswith(message)

        pattern = r"Original exception: Expected to read \d+ metadata " \
                  r"bytes, but only read \d+"
        assert re.search(pattern, error_message)


class TestDatasetModule:

    def test_dataset_contents(self, capsys, test_client,
                              package_request_index_v2,
                              dataset_request_index_v2,
                              instance_request_v1):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2,
            dataset_request_index_v2, instance_request_v1,
        ]

        pp = test_client.packages(search_term='', only_mine=False)
        ds = pp['Test Package'].datasets()
        d = ds['TestDataset']
        d.contents()
        captured = capsys.readouterr()
        assert captured.out == '\nINSTANCE 1 (size: 1.00 Mb)\n'

    @pytest.fixture()
    def return_value(self, dataset_request_index_v2):
        return partial(
            mock_catalogue_filter_search_response_impl,
            dataset_request_index_v2
        )

    def test_find_no_params(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets()) == 2

    def test_find_datasets_no_list(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=[])) == 2

    def test_find_datasets_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(only_mine=False)) == 2

    def test_find_datasets_only_mine(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(only_mine=True)) == 1

    def test_find_datasets_no_search_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=None, only_mine=False)) \
               == 2

    def test_find_datasets_no_list_all_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=[], only_mine=False)) == 2

    def test_find_datasets_no_term_only_mine(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=None, only_mine=True)) == 1

    def test_find_datasets_no_list_only_mine(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(search_term=[], only_mine=True)) == 1

    def test_find_datasets_ignore_bad_data_list(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["baddata"], only_mine=False)) == 2

    def test_find_datasets_ignore_multi_bad_data(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["baddata", "baddata"], only_mine=False)) == 2

    def test_find_datasets_ignore_bad_keep_good_data(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        assert len(
            test_client.datasets(
                search_term=["short_code=TestDataset", "baddata"],
                only_mine=False
            )
        ) == 1

    def test_find_datasets_ignore_bad_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term="baddata", only_mine=False)) == 2

    def test_find_datasets_name_search_match(self, test_client, return_value):
        test_client._session.get = return_value
        # testing search term with only_mine param against valid search term
        assert len(test_client.datasets(
            search_term=["short_code=TestDataset"], only_mine=False)) == 1

    def test_find_datasets_no_search_my_data(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=[], only_mine=True)) == 1

    def test_find_datasets_no_match(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["short_code=NotTestDataset"], only_mine=True)) == 0

    def test_find_datasets_multi_param_my_data(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        # multi-param against only_mine
        assert len(test_client.datasets(
            search_term=["name=Other Dataset"],
            only_mine=True)) == 0

    def test_find_datasets_multi_param_all_data(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["name=Test DataSet", "description=description",
                         "organisation_name=IHS Markit"],
            only_mine=False)) == 1

    def test_find_datasets_find_both(self, test_client, return_value):
        test_client._session.get = return_value
        assert len(test_client.datasets(
            search_term=["description=description"],
            only_mine=False)) == 2

    def test_find_datasets_multi_param_no_match(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        # multi-param with bad data
        assert len(test_client.datasets(
            search_term=[
                "description=description",
                "organisation_name=baddata"
            ],
            only_mine=False)) == 0

    def test_find_datasets_like_name(self, test_client, return_value):
        test_client._session.get = return_value
        # 'like' test
        assert len(test_client.datasets(
            search_term=["name like Test"],
            only_mine=True)) == 1

    def test_find_datasets_by_id(self, test_client, return_value):
        test_client._session.get = return_value
        # 'like' test
        assert len(test_client.datasets(
            search_term=["id=5b01376e-975d-11e9-8832-7e5ef76d533f"],
            only_mine=True)) == 1

    def test_find_datasets_override_has_access_return_none(
        self,
        test_client,
        return_value
    ):
        test_client._session.get = return_value
        # test override of param against kwarg of same (accomplish both ways)
        assert len(test_client.datasets(
            search_term=["has_access=True"],
            only_mine=False)) == 0

    def test_datasets_called_twice(self, test_client, package_request_index_v2,
                                   dataset_request_index_v2):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2, dataset_request_index_v2
        ]
        pp = test_client.packages(search_term='', only_mine=False)

        # This should work twice
        assert pp['Test Package'].datasets()
        assert pp['Test Package'].datasets()

    def test_retrieve_instance_given_package_dataset(self, test_client,
                                                     package_request_index_v2,
                                                     dataset_request_index_v2,
                                                     instance_request_v1
                                                     ):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2,
            dataset_request_index_v2, instance_request_v1,
        ]

        pp = test_client.packages(search_term='', only_mine=False)
        ds = pp['Test Package'].datasets()
        d = ds['TestDataset']
        instances = list(d.instances.all())
        assert (len(instances) == 1)
        assert (instances[0].datafile_id == 1)

    def test_retrieve_dataset_by_get(
        self,
        test_client,
        visible_orgs_v2,
        unstructured_dataset_request_index_v2
    ):
        test_client._session.get.return_value.json.side_effect = [
            visible_orgs_v2,
            unstructured_dataset_request_index_v2,
        ]

        test_ds = test_client.datasets.get('TestDataset')
        assert test_ds.short_code == "TestDataset"
