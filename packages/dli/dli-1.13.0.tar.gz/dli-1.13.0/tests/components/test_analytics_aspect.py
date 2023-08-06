import pytest

from unittest.mock import MagicMock, Mock

from dli.client.components import AnalyticsAspect


@pytest.fixture
def analytics_handler():
    yield Mock()


@pytest.fixture
def wrapped_object(analytics_handler):
    obj = Mock()
    obj._analytics_handler = analytics_handler
    yield obj


@pytest.fixture
def metadata():
    return {
        'subject': 'sub', 'organisation_id': 'org_id',
        'func': MagicMock(__qualname__='Dataset.get', __name__='get'),
        'arguments': {'why_not': 42}, 'kwargs': {}
    }


class TestLoggingAspect:

    analytics_aspect = AnalyticsAspect()

    def test_does_not_create_event_pre_call_if_handler_exists(
        self, wrapped_object
    ):
        self.analytics_aspect.invoke_pre_call_aspects(wrapped_object, {})

        assert wrapped_object._analytics_handler.create_event.call_count == 0

    def test_does_not_create_event_pre_call_if_handler_not_defined(
        self, wrapped_object
    ):
        wrapped_object._analytics_handler = MagicMock(
            __bool__=Mock(return_value=False)
        )
        self.analytics_aspect.invoke_pre_call_aspects(wrapped_object, {})

        assert wrapped_object._analytics_handler.create_event.call_count == 0

    def test_creates_event_post_call_if_handler_exists(
        self, wrapped_object, metadata
    ):
        self.analytics_aspect.invoke_post_call_aspects(wrapped_object, metadata)

        wrapped_object._analytics_handler.create_event\
            .assert_called_once_with(
                'sub', 'org_id', 'Dataset', 'get', {'why_not': 42},
                result_status_code=200
            )

    def test_does_not_create_event_post_call_if_handler_not_defined(
        self, wrapped_object
    ):
        wrapped_object._analytics_handler = MagicMock(
            __bool__=Mock(return_value=False)
        )

        self.analytics_aspect.invoke_post_call_aspects(
            wrapped_object, {}
        )

        assert wrapped_object._analytics_handler.create_event.call_count == 0

    def test_creates_event_after_specific_exception_if_handler_exists(
            self, wrapped_object, metadata
    ):
        exception = Mock()
        exception.response.status_code = 404
        self.analytics_aspect.invoke_after_exception_aspects(
            wrapped_object, metadata, exception
        )

        wrapped_object._analytics_handler.create_event\
            .assert_called_once_with(
                'sub', 'org_id', 'Dataset', 'get', {'why_not': 42},
                result_status_code=404
            )

    def test_creates_event_after_unknown_exception_if_handler_exists(
            self, wrapped_object, metadata
    ):
        exception = Mock()
        exception.response = None
        self.analytics_aspect.invoke_after_exception_aspects(
            wrapped_object, metadata, exception
        )

        wrapped_object._analytics_handler.create_event\
            .assert_called_once_with(
                'sub', 'org_id', 'Dataset', 'get', {'why_not': 42},
                result_status_code=500
            )

    def test_does_not_create_event_after_exception_if_handler_not_defined(
            self, wrapped_object
    ):
        wrapped_object._analytics_handler = MagicMock(
            __bool__=Mock(return_value=False)
        )

        self.analytics_aspect.invoke_after_exception_aspects(
            wrapped_object, {}, None
        )

        assert wrapped_object._analytics_handler.create_event.call_count == 0
