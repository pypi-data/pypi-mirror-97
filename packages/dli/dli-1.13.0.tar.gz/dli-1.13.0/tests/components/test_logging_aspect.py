import pytest

from unittest.mock import MagicMock, Mock

from dli.client.components import LoggingAspect


@pytest.fixture
def logger():
    yield Mock()


@pytest.fixture
def wrapped_object(logger):
    obj = Mock()
    obj.logger = logger
    yield obj


@pytest.fixture
def metadata():
    yield Mock()


class TestLoggingAspect:

    logging_aspect = LoggingAspect()

    def test_logs_info_pre_call_if_logger_exists(
        self, wrapped_object, metadata
    ):
        self.logging_aspect.invoke_pre_call_aspects(wrapped_object, metadata)

        wrapped_object.logger.debug.assert_called_once_with(
            'Client Function Called', extra=metadata
        )
        assert wrapped_object.logger.warning.call_count == 0
        assert wrapped_object.logger.debug.call_count == 1
        assert wrapped_object.logger.error.call_count == 0
        assert wrapped_object.logger.exception.call_count == 0

    def test_does_not_log_anything_pre_call_if_logger_not_defined(
        self, wrapped_object, metadata
    ):
        wrapped_object.logger = MagicMock(__bool__=Mock(return_value=False))
        self.logging_aspect.invoke_pre_call_aspects(wrapped_object, metadata)

        assert wrapped_object.logger.warning.call_count == 0
        assert wrapped_object.logger.info.call_count == 0
        assert wrapped_object.logger.debug.call_count == 0
        assert wrapped_object.logger.error.call_count == 0
        assert wrapped_object.logger.exception.call_count == 0

    def test_does_not_log_anything_post_call_if_logger_exists(
        self, wrapped_object, metadata
    ):
        self.logging_aspect.invoke_post_call_aspects(wrapped_object, metadata)

        assert wrapped_object.logger.warning.call_count == 0
        assert wrapped_object.logger.info.call_count == 0
        assert wrapped_object.logger.debug.call_count == 0
        assert wrapped_object.logger.error.call_count == 0
        assert wrapped_object.logger.exception.call_count == 0

    def test_does_not_log_anything_post_call_if_logger_not_defined(
        self, wrapped_object, metadata
    ):
        wrapped_object.logger = MagicMock(__bool__=Mock(return_value=False))
        self.logging_aspect.invoke_pre_call_aspects(wrapped_object, metadata)

        assert wrapped_object.logger.warning.call_count == 0
        assert wrapped_object.logger.info.call_count == 0
        assert wrapped_object.logger.debug.call_count == 0
        assert wrapped_object.logger.error.call_count == 0
        assert wrapped_object.logger.exception.call_count == 0

    def test_logs_exception_after_exception_post_call_if_logger_exists(
            self, wrapped_object, metadata, monkeypatch
    ):
        inspect_mock = Mock(trace=Mock(return_value=[[Mock(f_locals='abc')]]))
        monkeypatch.setattr('dli.client.aspects.inspect', inspect_mock)

        self.logging_aspect.invoke_after_exception_aspects(
            wrapped_object, metadata, None
        )

        wrapped_object.logger.exception.assert_called_once_with(
            'Unhandled Exception', stack_info=False, extra={
                    'locals': 'abc'
                }
        )
        assert wrapped_object.logger.warning.call_count == 0
        assert wrapped_object.logger.info.call_count == 0
        assert wrapped_object.logger.debug.call_count == 0
        assert wrapped_object.logger.error.call_count == 0

    def test_does_not_log_anything_after_exception_if_logger_not_defined(
            self, wrapped_object, metadata
    ):
        wrapped_object.logger = MagicMock(__bool__=Mock(return_value=False))
        self.logging_aspect.invoke_after_exception_aspects(
            wrapped_object, metadata, None
        )

        assert wrapped_object.logger.warning.call_count == 0
        assert wrapped_object.logger.info.call_count == 0
        assert wrapped_object.logger.debug.call_count == 0
        assert wrapped_object.logger.error.call_count == 0
        assert wrapped_object.logger.exception.call_count == 0
