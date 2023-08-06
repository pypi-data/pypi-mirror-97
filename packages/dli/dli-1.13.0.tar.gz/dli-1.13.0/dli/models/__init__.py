#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import contextlib
import inspect
import warnings
from collections import UserDict
from typing import Mapping

from dli.client.components.urls import dataset_urls


def log_public_functions_calls_using(decorators, class_fields_to_log=None):
    if not class_fields_to_log:
        class_fields_to_log = []

    def decorate(cls):
        functions_to_exclude = inspect.getmembers(AttributesDict, inspect.isfunction)
        functions_to_decorate = [
            func for func in inspect.getmembers(cls, inspect.isfunction)
            if func not in functions_to_exclude and not func[0].startswith('_') and not func[0].startswith('__')
        ]
        for function_meta in functions_to_decorate:
            function_name = function_meta[0]
            for decorator in decorators:
                setattr(
                    cls,
                    function_name,
                    decorator(getattr(cls, function_name),
                              class_fields_to_include=class_fields_to_log)
                )
        return cls
    return decorate


class SampleData:
    def __init__(self, parent):
        self._parent = parent
        self._client = parent._client

    def schema(self):
        """
        Returns the schema data and first rows of sample data.

        :returns: attributes dictionary
        """
        response = self._client.session.get(
            dataset_urls.v2_sample_data_schema.format(id=self._parent.id)
        )

        return AttributesDict(**response.json()['data']['attributes'])

    @contextlib.contextmanager
    def file(self):
        """
        Provides a file like object containing sample data.

        Example usage:

        .. code-block:: python

            dataset = self.client.get_dataset(dataset_id)
            with dataset.sample_data.file() as f:
                dataframe = pandas.read_csv(f)
        """
        response = self._client.session.get(
            dataset_urls.v2_sample_data_file.format(id=self._parent.id),
            stream=True
        )
        # otherwise you get raw secure
        response.raw.decode_content = True
        yield response.raw
        response.close()


class AttributesDict(UserDict):

    def __init__(self, *args, **kwargs):
        # recursively provide the rather silly attribute
        # access
        data = {}

        for arg in args:
            data.update(arg)

        data.update(**kwargs)

        for key, value in data.items():
            if isinstance(value, Mapping):
                self.__dict__[key] = AttributesDict(value)
            else:
                self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        attributes = ' '.join([
            '{}={}'.format(k, v) for k,v in self.__dict__.items()
            if not k.startswith('_')
        ])

        return "{}({})".format(self.__class__.__name__, attributes)
