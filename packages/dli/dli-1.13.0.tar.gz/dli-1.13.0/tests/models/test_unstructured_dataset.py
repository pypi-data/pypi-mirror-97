from unittest.mock import MagicMock, call

import pytest
from s3transfer.futures import TransferFuture

from dli.models.unstructured_dataset_model import UnstructuredDatasetModel
from dli.models.structured_dataset_model import StructuredDatasetModel


class TestUnstructuredDataset:

    def __setup_mocks(
        self,
        monkeypatch,
    ):
        # This has a directory name starting with `.` so must be ignored.
        self.key_latest_0 = MagicMock()
        self.key_latest_0.key = 'abc/.latest/nulls_and_unicode.parquet'
        self.key_latest_0.size = 1

        self.key_document1_attachment_0 = MagicMock()
        self.key_document1_attachment_0.key = 'abc/document_id=1/attachment/0.zip'
        self.key_document1_attachment_0.size = 1
        self.key_document1_document_0 = MagicMock()
        self.key_document1_document_0.key = 'abc/document_id=1/document/0.xml'
        self.key_document1_document_0.size = 1
        self.key_document1_document_1 = MagicMock()
        self.key_document1_document_1.key = 'abc/document_id=1/document/0.parquet'
        self.key_document1_document_1.size = 1
        self.key_document1_metadata_0 = MagicMock()
        self.key_document1_metadata_0.key = 'abc/document_id=1/metadata/0.json'
        self.key_document1_metadata_0.size = 1

        self.key_document2_attachment_0 = MagicMock()
        self.key_document2_attachment_0.key = 'abc/document_id=2/attachment/0.zip'
        self.key_document2_attachment_0.size = 1
        self.key_document2_document_0 = MagicMock()
        self.key_document2_document_0.key = 'abc/document_id=2/document/0.xml'
        self.key_document2_document_0.size = 1
        self.key_document2_document_1 = MagicMock()
        self.key_document2_document_1.key = 'abc/document_id=2/document/0.parquet'
        self.key_document2_document_1.size = 1
        self.key_document2_metadata_0 = MagicMock()
        self.key_document2_metadata_0.key = 'abc/document_id=2/metadata/0.json'
        self.key_document2_metadata_0.size = 1

        self.filter_mock = MagicMock()
        self.filter_mock.side_effect = iter([
            [
                self.key_latest_0,
                self.key_document1_attachment_0,
                self.key_document1_document_0,
                self.key_document1_document_1,
                self.key_document1_metadata_0,
                self.key_document2_attachment_0,
                self.key_document2_document_0,
                self.key_document2_document_1,
                self.key_document2_metadata_0,
            ]
        ])

        self.objects_mock = MagicMock()
        self.objects_mock.return_value.filter = self.filter_mock

        self.bucket_mock = MagicMock()
        self.bucket_mock.return_value.objects = self.objects_mock()

        self.resource_mock = MagicMock()
        self.resource_mock.return_value.Bucket = self.bucket_mock

        self.resource_mock.return_value.meta.client.list_objects_v2.return_value = {
            'CommonPrefixes': [
                {'Prefix': 'abc/.latest/'},
                {'Prefix': 'abc/document_id=1/'},
                {'Prefix': 'abc/document_id=2/'},
            ]
        }

        self.boto_mock = MagicMock()
        self.boto_mock.return_value.resource.return_value = self.resource_mock()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            self.boto_mock
        )

        self.transfer_future_mock = MagicMock(return_value=TransferFuture())
        self.transfer_future_mock.return_value.result = True
        self.download_mock = MagicMock()
        self.download_mock.download = lambda x: self.transfer_future_mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            self.download_mock
        )

    def assert_calls(self):
        self.boto_mock.assert_called()
        self.resource_mock.assert_called_once()
        self.bucket_mock.assert_has_calls([
            call('abc')
        ])
        self.objects_mock.assert_called_once()
        self.filter_mock.assert_has_calls([
            # Assert that we only call the non-hidden prefixes.
            call(Prefix='abc/'),
        ])

    def test_model_factory_instantiation(self, test_client, unstructured_dataset_request_index_v2):
        test_client._session.get.return_value.json.side_effect = [
            unstructured_dataset_request_index_v2,
        ]

        test_ds = test_client.datasets()

        assert type(test_ds.get("TestDataset")).__name__ == UnstructuredDatasetModel.__name__
        assert type(test_ds.get("OtherDataset")).__name__ == StructuredDatasetModel.__name__

    def test_list_plain(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.list()

        self.assert_calls()

        assert len(ls) == 9, f'List: {ls}'

    def test_list_method_with_structured_args(self, object_summaries_s3, monkeypatch, client):
        class MockResource:
            class Objects:
                def filter(self, Prefix):
                    return object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with pytest.raises(AttributeError) as e_info:
            dataset.list(partitions=["document_id=1"])
        assert "EXISTS" in str(e_info.value.args[0])

    def test_none_existing_method(self, object_summaries_s3, monkeypatch, client):

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with pytest.raises(AttributeError) as e_info:
            dataset.dask_dataframe()
        assert "EXISTS" not in str(e_info.value.args[0])

    def test_download_plain(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test")

        self.assert_calls()

        assert len(ls) == 8, f'List: {ls}'

    def test_download_method_with_structured_args(self, unstructured_object_summaries_s3, monkeypatch, client):
        class MockResource:
            name = 'some-bucket'

            class Objects:
                def filter(self, Prefix):
                    return unstructured_object_summaries_s3

            def Bucket(self, *args):
                return self

            @property
            def meta(self):
                return MagicMock()

            @property
            def objects(self):
                objects = MockResource.Objects()
                return objects

        boto_mock = MagicMock()
        boto_mock.return_value.resource.return_value = MockResource()
        monkeypatch.setattr(
            'dli.models.dataset_model.create_refreshing_session',
            boto_mock
        )

        mock = MagicMock(return_value=TransferFuture())
        mock.return_value.result = True
        download_mock = MagicMock()
        download_mock.download = lambda x: mock
        monkeypatch.setattr(
            'dli.models.dataset_model.DatasetModel._get_transfer_manager',
            download_mock
        )

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        with pytest.raises(AttributeError) as e_info:
            dataset.download("test", flatten=True, partitions="document_id=1")
        assert "EXISTS" in str(e_info.value.args[0])

    def test_download_filter_attachments_plain(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test", with_attachments=False)

        self.assert_calls()

        assert all(map(lambda x: "attachment" not in x, ls))
        assert len(ls) == 6

    def test_download_filter_metadata(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test", with_metadata=False)

        self.assert_calls()

        assert all(map(lambda x: "metadata" not in x, ls))
        assert len(ls) == 6

    def test_download_filter_attachments_and_metadata(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        ls = dataset.download("test", with_attachments=False, with_metadata=False)

        self.assert_calls()

        assert all(map(lambda x: "attachment" not in x and "metadata" not in x, ls))
        assert len(ls) == 4

    def test_download_filter_only_documents(self, monkeypatch, client):
        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # type exist list
        self.__setup_mocks(monkeypatch)
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types=["xml"])

        self.assert_calls()

        assert all(map(lambda x: ".xml" in x, ls))

        # mix type exist/not exist list
        self.__setup_mocks(monkeypatch)
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types=["xml", "html"])

        self.assert_calls()

        assert all(map(lambda x: ".xml" in x, ls))

        # type not exist
        self.__setup_mocks(monkeypatch)
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types="html")

        self.assert_calls()

        assert len(ls) == 0

        # type exist list 2
        self.__setup_mocks(monkeypatch)
        ls = dataset.download("test", with_attachments=False, with_metadata=False,
                              document_types=["xml", "parquet"])

        self.assert_calls()

        assert all(map(lambda x: ".xml" in x or ".parquet" in x, ls))
        assert len(ls) == 4

    def test_download_skip_zero_document_folders(self,
                                                 monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        self.filter_mock.side_effect = iter([
            [
                self.key_latest_0,
                self.key_document1_attachment_0,
                # Removed the document from here!
                self.key_document1_metadata_0,
                self.key_document2_attachment_0,
                self.key_document2_document_0,
                self.key_document2_document_1,
                self.key_document2_metadata_0,
            ]
        ])

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # there are only attachment and metadata in document_id=2
        ls = dataset.download(
            "test",
            skip_folders_with_zero_matching_documents=True
        )

        self.assert_calls()

        assert all(['document_id=2' in x for x in ls]), f'List: {ls}'
        assert len([x for x in ls if 'document_id=1' in x]) == 0, \
            f'Excepted 0 for document_id=1. List: {ls}'
        assert len([x for x in ls if 'document_id=2' in x]) == 4, \
            f'Excepted 4 for document_id=2. List: {ls}'

        self.__setup_mocks(monkeypatch)

        self.filter_mock.side_effect = iter([
            [
                self.key_latest_0,
                self.key_document1_attachment_0,
                # Removed the document from here!
                self.key_document1_metadata_0,
                self.key_document2_attachment_0,
                self.key_document2_document_0,
                self.key_document2_document_1,
                self.key_document2_metadata_0,
            ]
        ])

        ls = dataset.download(
            "test",
            skip_folders_with_zero_matching_documents=False
        )

        self.assert_calls()

        assert any(['document_id=2' in x for x in ls])
        assert len([x for x in ls if 'document_id=1' in x]) == 2, \
            'Excepted 2 for document_id=1'
        assert len([x for x in ls if 'document_id=2' in x]) == 4, \
            'Excepted 4 for document_id=2'

    def test_download_metadata(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # there are only attachment and metadata in document_id=3
        ls = dataset.download_metadata("test")

        self.assert_calls()

        assert all(map(lambda x: "metadata" in x or '.latest' in x, ls)), \
            f'List: {ls}'

    def test_download_attachments(self, monkeypatch, client):
        self.__setup_mocks(monkeypatch)

        dataset = client._DatasetFactory._from_v2_response({
            'data': {
                'id': '1234',
                'attributes': {
                    'content_type': 'Unstructured',
                    'location': {},
                    'organisation_short_code': 'abc',
                    'short_code': 'abc',
                    'has_access': True,
                }
            }
        })

        # there are only attachment and metadata in document_id=3
        ls = dataset.download_attachments("test")

        self.assert_calls()

        assert all(map(lambda x: "attachment" in x or '.latest' in x, ls)), \
            f'List: ls'


    #check against dl-5214
