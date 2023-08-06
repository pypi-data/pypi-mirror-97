from unittest.mock import Mock

import time
import pytest

import dli
from dli.analytics import AnalyticsHandler


@pytest.fixture
def dli_client():
    session = Mock()
    session.has_expired = False

    environment = Mock(consumption='http://someurl')
    return Mock(_session=session, _environment=environment)


class TestAnalyticsHandler:

    def test_properly_creates_handler(self):
        logger = Mock()
        dli_client = Mock(logger=logger)
        analytics_handler = AnalyticsHandler(dli_client)
        assert analytics_handler._app_name == 'SDK'
        assert analytics_handler._app_version == dli.__version__
        assert analytics_handler._client == dli_client

    def test_handles_internal_exceptions(self, dli_client):
        exception_to_be_thrown = ValueError()
        dli_client.session.post.side_effect = exception_to_be_thrown
        dli_client.strict = True

        analytics_handler = AnalyticsHandler(dli_client)
        for _ in range(11):
            analytics_handler.create_event('user', 'org', properties={})

        time.sleep(0.1)
        dli_client.session.post.assert_called_once()
        dli_client.logger.exception.assert_called_once_with(
            'Error while sending analytics: ', exception_to_be_thrown
        )

    def test_sends_proper_message_on_proper_input(self, dli_client):
        analytics_handler = AnalyticsHandler(dli_client)
        for _ in range(11):
            analytics_handler.create_event('user', 'org', properties={})
        time.sleep(0.1)
        assert len(dli_client.session.post.call_args[1]['json']['data']) == 11

    def test_sends_message_with_filtered_out_properties(self, dli_client):
        analytics_handler = AnalyticsHandler(dli_client)
        properties = {
            'package_id': '1',
            'dataset_id': '2',
            'name': 'some_name',
            'dataset_name': 'd_name',
            'datafile_id': 'datafile_id',
            'dictionary_id': 'dictionary_id',
            'api_key': 'key',
            'unknown': 'property'
        }
        for _ in range(11):
            analytics_handler.create_event('user', 'org', properties={})

        time.sleep(0.1)

        properties.pop('unknown')
        assert len(dli_client.session.post.call_args[1]['json']['data']) == 11

    def test_event_not_sent_when_client_has_expired(self, dli_client):
        dli_client._session.has_expired = True

        analytics_handler = AnalyticsHandler(dli_client)
        properties = {
            'package_id': '1',
            'dataset_id': '2',
            'name': 'some_name',
            'dataset_name': 'd_name',
            'datafile_id': 'datafile_id',
            'dictionary_id': 'dictionary_id',
            'api_key': 'key',
            'unknown': 'property'
        }
        properties.pop('unknown')

        for _ in range(11):
            analytics_handler.create_event('user', 'org', properties={})

        time.sleep(0.1)

        dli_client._session.post.assert_not_called()
