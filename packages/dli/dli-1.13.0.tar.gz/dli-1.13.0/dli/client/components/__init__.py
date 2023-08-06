#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import types
from functools import wraps

from dli.client.aspects import extract_metadata, LoggingAspect, AnalyticsAspect
from dli.siren import siren_to_entity


class ComponentsAspectWrapper(type):
    """
    This decorates all functions in a Component with a logging function.
    """
    __aspects = [LoggingAspect(), AnalyticsAspect()]

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if (
                isinstance(attr_value, types.FunctionType)
                and not attr_name.startswith('_')
            ):
                attrs[attr_name] = cls._wrap_call_with_aspects(attr_value)

        return super(ComponentsAspectWrapper, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def _wrap_call_with_aspects(cls, func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                metadata = extract_metadata(self, self, func, args, kwargs)
            except Exception as e:
                if getattr(self, 'logger', None):
                    self.logger.exception(
                        'Error while reading function metadata.', e
                    )
                return func(self, *args, **kwargs)

            try:
                cls._invoke_pre_call_aspects(self, metadata)
                result = func(self, *args, **kwargs)
                cls._invoke_post_call_aspects(self, metadata)
                return result
            except Exception as e:
                # If the object contains a `strict` boolean and it is set to
                # True, then print out the exception message and a full stack
                # trace.
                # DEFAULTED to True to match the current behaviour. This default
                # can be changed in a later release. When we change the default
                # we will have to update the tests to explicitly set strict to
                # True to maintain the previous test behaviour.
                if getattr(self, 'strict', True):
                    cls._invoke_after_exception_aspects(self, metadata, e)
                    raise e
                else:
                    # Data scientists do not want to see stack dumps by
                    # default, especially when we have a root cause that
                    # triggers secondary exceptions.
                    self.logger.warning(
                        '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                        '\nAn exception occurred so we are returning None.'
                        '\nTo see the exception and stack trace, please start '
                        'the session again with the parameter `strict=True`'
                        '\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                    )
                    return None

        return wrapper

    @classmethod
    def _invoke_pre_call_aspects(cls, wrapped_object, metadata):
        for aspect in cls.__aspects:
            aspect.invoke_pre_call_aspects(wrapped_object, metadata)

    @classmethod
    def _invoke_post_call_aspects(cls, wrapped_object, metadata):
        for aspect in cls.__aspects:
            aspect.invoke_post_call_aspects(wrapped_object, metadata)

    @classmethod
    def _invoke_after_exception_aspects(cls, wrapped_object, metadata, exception):
        for aspect in cls.__aspects:
            aspect.invoke_after_exception_aspects(wrapped_object, metadata, exception)


class SirenComponent(metaclass=ComponentsAspectWrapper):

    def __init__(self, client=None):
        self.client = client


class SirenAdapterResponse:

    # Helper class to wrap a response object.
    def __init__(self, response):
        self.response = response

    def to_siren(self):
        # Pypermedias terminology, not mine
        python_object = self.response.builder._construct_entity(
            self.response.json()
        ).as_python_object()

        # Keep the response availible
        python_object._raw_response = self

        return python_object

    def to_many_siren(self, relation):
        return [
            siren_to_entity(c) for c in
            self.to_siren().get_entities(rel=relation)
        ]