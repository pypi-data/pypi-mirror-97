#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import inspect
from functools import wraps


class LoggingAspect:

    @staticmethod
    def invoke_pre_call_aspects(wrapped_object, metadata):
        if getattr(wrapped_object, 'logger', None):
            try:
                wrapped_object.logger.debug('Client Function Called', extra=metadata)
            except Exception as e:
                wrapped_object.logger.exception(
                    'Error while invoking pre-call aspects.', e
                )

    @staticmethod
    def invoke_post_call_aspects(wrapped, metadata):
        pass

    @staticmethod
    def invoke_after_exception_aspects(wrapped_object, metadata, exception):
        if getattr(wrapped_object, 'logger', None):
            # If the object contains a `strict` boolean and it is set to
            # True, then print out the exception message and a full stack
            # trace.
            # DEFAULTED to True to match the current behaviour. This default
            # can be changed in a later release. When we change the default
            # we will have to update the tests to explicitly set strict to
            # True to maintain the previous test behaviour.
            if getattr(wrapped_object, 'strict', True):
                try:
                    wrapped_object.logger.exception(
                        'Unhandled Exception', stack_info=False, extra={
                            'locals': inspect.trace()[-1][0].f_locals
                        })
                except Exception as e:
                    wrapped_object.logger.exception(
                        'Error while invoking pre-call aspects.', e
                    )
            else:
                # Data scientists do not want to see stack dumps by default,
                # especially when we have a root cause that triggers secondary
                # exceptions.
                wrapped_object.logger.warning(
                    '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
                    '\nAn exception occurred so we are returning None.'
                    '\nTo see the exception and stack trace, please start '
                    'the session again with the parameter `strict=True`'
                    '\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
                )


class AnalyticsAspect:

    @staticmethod
    def invoke_pre_call_aspects(wrapped_object, metadata):
        pass

    def invoke_post_call_aspects(self, wrapped_object, metadata):
        if getattr(wrapped_object, '_analytics_handler', None):
            try:
                self._create_event(wrapped_object, metadata, status_code=200)
            except Exception as e:
                wrapped_object.logger.exception(
                    'Error while invoking post-call aspects.', e
                )

    def invoke_after_exception_aspects(self, wrapped_object, metadata, exception):
        if getattr(wrapped_object, '_analytics_handler', None):
            try:
                status_code = self._retrieve_status_code_from_exception(exception)
                self._create_event(wrapped_object, metadata, status_code=status_code)
            except Exception as e:
                wrapped_object.logger.exception(
                    'Error while invoking after-exception aspects.', e
                )

    @staticmethod
    def _create_event(dli_client, metadata, status_code):
        additional_properties = metadata.get('properties') or {}
        dli_client._analytics_handler.create_event(
            metadata['subject'], metadata['organisation_id'],
            metadata['func'].__qualname__.split('.')[0],
            metadata['func'].__name__,
            {**metadata['arguments'], **metadata['kwargs'], **additional_properties},
            result_status_code=status_code
        )

    @staticmethod
    def _retrieve_status_code_from_exception(exception):
        try:
            return exception.response.status_code
        except AttributeError:
            return 500


def analytics_decorator(function, class_fields_to_include):
    aspect = AnalyticsAspect()

    @wraps(function)
    def function_wrapper(target, *args, **kwargs):
        metadata = extract_metadata(
            target._client, target, function, args, kwargs, class_fields_to_include
        )

        aspect.invoke_pre_call_aspects(target._client, metadata)
        try:
            result = function(target, *args, **kwargs)
        except TypeError as t:
            # its a pity to put this here, but we need to hijack TypeError for UnstructuredDatasetModel
            # we can't use hasattr, since the TypeError hijack will return something!
            # N.B. if you need to see the real cause, comment out the _type_exception_handler of the class.
            if "_type_exception_handler" in dir(target):
                target._type_exception_handler(t, function, args, kwargs)
                return
            else:
                aspect.invoke_after_exception_aspects(target._client, metadata, t)
                raise t

        except Exception as e:
            aspect.invoke_after_exception_aspects(target._client, metadata, e)
            raise e
        aspect.invoke_post_call_aspects(target._client, metadata)
        return result

    return function_wrapper


def logging_decorator(function, class_fields_to_include):
    aspect = LoggingAspect()

    @wraps(function)
    def function_wrapper(target, *args, **kwargs):
        metadata = extract_metadata(
            target._client, target, function, args, kwargs, class_fields_to_include
        )
        aspect.invoke_pre_call_aspects(target._client, metadata)
        try:
            result = function(target, *args, **kwargs)
        except Exception as e:
            aspect.invoke_after_exception_aspects(target._client, metadata, e)
            raise e
        aspect.invoke_post_call_aspects(target._client, metadata)
        return result

    return function_wrapper


def extract_metadata(
        dli_client, wrapped_object, func, arguments,
        keyword_args, class_fields_to_include=None
):
    # Get the user calling the function
    org_id, subject = _retrieve_user_details(dli_client)

    # This is to find out what the 'arg' names are.
    argspec = inspect.getfullargspec(func)
    args_dict = dict(zip(argspec.args, [wrapped_object, *arguments]))

    properties = _read_field_values(class_fields_to_include, wrapped_object)

    if not subject:
        if args_dict.get('api_key'):
            subject = '***' + args_dict.get('api_key')[:6]
        else:
            subject = 'UNKNOWN USER'

    return {
        'func': func,
        'subject': subject,
        'organisation_id': org_id,
        'arguments': args_dict,
        'kwargs': dict(keyword_args),
        'properties': properties
    }


def _retrieve_user_details(dli_client):
    org_id = None
    user_id = getattr(dli_client, 'api_key', '')[:6]
    try:
        org_id = dli_client.session.decoded_token.get('datalake').get('organisation_id')
        user_id = dli_client.session.decoded_token.get('sub', 'UNKNOWN USER')
    except AttributeError:
        pass

    return org_id, user_id


def _read_field_values(class_fields_to_include, wrapped_object):
    properties = {}
    for field in class_fields_to_include or []:
        property_name = field.split('.')[-1]
        property_value = wrapped_object
        for nested_field_name in field.split('.'):
            property_value = property_value.__dict__[nested_field_name]
        properties.update({property_name: property_value})
    return properties
