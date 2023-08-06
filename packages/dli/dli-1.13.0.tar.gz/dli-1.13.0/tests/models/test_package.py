from functools import partial
from unittest.mock import MagicMock
from tests.models.conftest import mock_catalogue_filter_search_response_impl


class TestPackageModel:
    def test_display_package(
        self, capsys, dataset_request_index_v2, test_client,
        package_request_v2
    ):
        test_client._session.get.return_value.json.side_effect = [
            dataset_request_index_v2
        ]

        package = test_client._Package(package_request_v2)
        package.contents()
        captured = capsys.readouterr()
        assert captured.out.startswith(
            '\nDATASET "TestDataset" [PARQUET]\n'
            '>> Shortcode: TestDataset\n'
            '>> Available Date Range: 2019-05-06 to 2020-01-01\n'
            '>> ID: 5b01376e-975d-11e9-8832-7e5ef76d533f\n'
            '>> Published: Monthly by IHS Markit\n'
        )

    def test_retrieve_datasets_given_package(self, test_client,
                                             package_request_index_v2, package_request_v2,
                                             dataset_request_index_v2):
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2, dataset_request_index_v2
        ]

        pp = test_client.packages(search_term="", only_mine=False)
        ds = pp["Test Package"].datasets()
        assert len(ds) == 2


class TestPackageModule:

    def test_find_packages(
        self, test_client, package_request_index_v2
    ):


        test_client._session.get = partial(
            mock_catalogue_filter_search_response_impl,
            package_request_index_v2
        )

        assert len(test_client.packages()) == 2
        assert len(test_client.packages(search_term=[])) == 2
        assert len(test_client.packages(only_mine=False)) == 2
        assert len(test_client.packages(only_mine=True)) == 1
        assert len(test_client.packages(search_term=None, only_mine=False)) == 2
        assert len(test_client.packages(search_term=[], only_mine=False)) == 2
        assert len(test_client.packages(search_term=None, only_mine=True)) == 1
        assert len(test_client.packages(search_term=[], only_mine=True)) == 1

        # bad data is ignored (we filter that out before the send)
        assert len(test_client.packages(
            search_term=["baddata"], only_mine=False)) == 2
        assert len(test_client.packages(
            search_term=["baddata", "baddata"], only_mine=False)) == 2
        assert len(test_client.packages(
            search_term=["name=Test Package", "baddata"], only_mine=False)) == 1
        assert len(test_client.packages(
            search_term="baddata", only_mine=False)) == 2

        # testing search term with only_mine param against valid search term
        assert len(test_client.packages(
            search_term=["name=Test Package"], only_mine=False)) == 1
        assert len(test_client.packages(
            search_term=[], only_mine=True)) == 1
        assert len(test_client.packages(
            search_term=["name=Not a Package"], only_mine=True)) == 0

        # multi-param against only_mine
        assert len(test_client.packages(
            search_term=["name=Different Name", "topic=Finance",
                         "organisation_name=Test Org"],
            only_mine=True)) == 0
        assert len(test_client.packages(
            search_term=["name=Different Name", "topic=Finance",
                         "organisation_name=Test Org"],
            only_mine=False)) == 1
        assert len(test_client.packages(
            search_term=["name=Test Package", "topic=Climate",
                         "organisation_name=IHS Markit"],
            only_mine=False)) == 1
        assert len(test_client.packages(
            search_term=["description=test-data"],
            only_mine=False)) == 2

        # multi-param with bad data
        assert len(test_client.packages(
            search_term=["description=test-data", "organisation_name=baddata"],
            only_mine=False)) == 0

        # 'like' test
        assert len(test_client.packages(
            search_term=["name like Test"],
            only_mine=True)) == 1

        # test override of param against kwarg of same (accomplish both ways)
        assert len(test_client.packages(
            search_term=["has_access=True"],
            only_mine=False)) == 0

    def test_retrieve_package_by_get(
        self, test_client, package_request_index_v2, dataset_request_index_v2
    ):

        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2
        ]

        test_package = test_client.packages.get('Test Package')
        assert test_package.name == "Test Package"
