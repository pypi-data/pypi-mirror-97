import copy
import pytest

from dli.models.paginator import Paginator


@pytest.fixture
def empty_package_request():
    return {
            "class": ["Access Requests", "collection"],
            "properties": {"page": 1, "pages_count": 1},
            "entities": []
           }


class TestPaginator:
    def test_retrieve_zero_packages(self, test_client, empty_package_request,
                                    dataset_request_v2):
        test_client._session.get.return_value.json.side_effect = [
            empty_package_request, dataset_request_v2
        ]

        paginator = Paginator(
            '/',
            test_client._Package,
        )

        assert len(list(paginator)) == 0

    def test_threaded_paginator(self, test_client,
                                package_request_index_v2):

        # Note: there is no side-effect call to dataset because the call that was
        # previously made in the constructor by .shape has now been made lazy to
        # avoid an explosion of calls.
        test_client._session.get.return_value.json.side_effect = [
            package_request_index_v2]

        paginator = Paginator(
            '/',
            test_client._Package,
            lambda a, page_size: {}
        )

        assert len(list(paginator)) == 2

