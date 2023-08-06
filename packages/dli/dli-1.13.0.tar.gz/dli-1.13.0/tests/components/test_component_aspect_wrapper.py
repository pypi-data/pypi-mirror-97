from unittest import mock

import pytest

from unittest.mock import Mock, MagicMock, call

from dli.client.components import ComponentsAspectWrapper
from dli.client.dli_client import DliClient


class Client(DliClient):

    def __init__(self):
        self.logger = MagicMock()
        session = Mock(
            decoded_token={'sub': 'sub', 'datalake': {'organisation_id': 'tid'}}
        )
        self._session = session

    @property
    def session(self):
        return self._session

    def test_function(self, attr1, attr2, attr3=None):
        pass

    def test_exception_function(self, attr1, attr2, attr3=None):
        raise ValueError('abc')


@pytest.fixture
def aspects():
    yield [Mock(), Mock()]


@pytest.fixture
def client(aspects):
    with mock.patch.object(
        ComponentsAspectWrapper, '_ComponentsAspectWrapper__aspects', aspects
    ):
        yield Client()


@pytest.fixture
def metadata(client):
    return {
        'func': Any(),
        'subject': 'sub',
        'organisation_id': 'tid',
        'arguments': {'self': client, 'attr1': 'val1', 'attr2': 'val2'},
        'kwargs': {'attr3': 'val3'},
        'properties': {}
    }


def Any():
    class Any:
        def __eq__(self, other):
            return True
    return Any()


class TestComponentsAspectWrapper:

    def test_calls_aspects_when_no_exception(self, client, aspects, metadata):
        expected_call = call(client, metadata)

        client.test_function('val1', 'val2', attr3='val3')

        # one call is for __init__ method, the other for the actual test_func
        assert aspects[0].invoke_pre_call_aspects.call_count == 1
        # assert aspects[0].invoke_pre_call_aspects.call_args_list[1] == expected_call
        assert aspects[0].invoke_post_call_aspects.call_count == 1
        # assert aspects[0].invoke_post_call_aspects.call_args_list[1] == expected_call
        assert aspects[0].invoke_after_exception_aspects.call_count == 0

        assert aspects[1].invoke_pre_call_aspects.call_count == 1
        # assert aspects[1].invoke_pre_call_aspects.call_args_list[1] == expected_call
        assert aspects[1].invoke_post_call_aspects.call_count == 1
        # assert aspects[1].invoke_post_call_aspects.call_args_list[1] == expected_call
        assert aspects[1].invoke_after_exception_aspects.call_count == 0

    def test_calls_aspects_when_exception_occurs(
            self, client, aspects, metadata
    ):
        expected_call_no_exception = call(client, metadata)

        with pytest.raises(ValueError) as e:
            client.test_exception_function('val1', 'val2', attr3='val3')


        expected_call_exception = call(client, metadata, e.value)

        assert aspects[0].invoke_pre_call_aspects.call_count == 1
        assert aspects[0].invoke_pre_call_aspects.call_args_list[0] == \
               expected_call_no_exception

        assert aspects[0].invoke_post_call_aspects.call_count == 0
        assert aspects[0].invoke_after_exception_aspects.call_count == 1
        assert aspects[0].invoke_after_exception_aspects.call_args_list[0] == \
               expected_call_exception
