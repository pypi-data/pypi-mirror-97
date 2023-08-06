#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import textwrap
import warnings
from collections import OrderedDict
from typing import Dict

from dli.client import utils
from dli.models.paginator import Paginator
from dli.client.components.urls import package_urls
from dli.models import AttributesDict
from dli.models.dataset_model import DatasetModel


class PackageModel(AttributesDict):
    """
    Represents a package pulled back from Me consumables
    """

    @classmethod
    def _raw_dict(cls, v1_response):
        return v1_response['properties']

    @classmethod
    def _from_v1_response_to_v2(cls, v1_response):
        response = cls._client.session.get(
            package_urls.v2_package_by_id.format(
                id=v1_response['properties']['packageId']
            )
        )
        json = response.json()
        return cls(json)

    @classmethod
    def _from_v2_response_unsheathed(cls, response_json, page_size=None):
        """

        :param response_json:
        :param page_size: Unused value, added to keep the same interface as
        datasetModel's _from_v2_response_unsheathed.
        :return:
        """

        return cls({
            'data': response_json
        })

    def __init__(self, json):
        # We have to declare the attribute `documentation` because it is
        # referenced in the code of this class. This means that there will
        # be an `documentation` attribute even when there is zero
        # `documentation` attribute in the Catalogue response JSON.
        self.documentation = None
        self.__shape = None

        # Maintain compatibility between V1 (which had package_id) and V2
        # (which only has ID).
        if 'package_id' not in json['data']['attributes']:
            json['data']['attributes']['package_id'] = json['data']['id']

        super().__init__(id=json['data']['id'], **json['data']['attributes'])
        self._paginator = Paginator(
            package_urls.v2_package_datasets.format(id=self.id),
            self._client._DatasetFactory,
            self._client._DatasetFactory._from_v2_response_unsheathed
        )

    @property
    def shape(self):
        """
        :returns: Count the number of datasets.
        :rtype: Int
        """
        if self.__shape is None:
            self.__shape = len(self.datasets())
        return self.__shape

    def datasets(self) -> Dict[str, DatasetModel]:
        """
        :returns: Dictionary of datasets in a package.
        :rtype: OrderedDict[id: str, DatasetModel]
        """
        return OrderedDict([
            (v.short_code, v) for v in self._paginator
        ])

    def contents(self):
        """Print information about all the datasets in this package."""
        for p in self.datasets().items():
            print(str(p[1]))

    def metadata(self):
        """
        Once you have selected a package, you can print the metadata
        (the available fields and values).

        :example:

            .. code-block:: python
                # Get all packages.
                >>> packages = client.packages('example package')
                # Get metadata of the 'example package' package.
                >>> packages['example package'].metadata()

        :example:

            .. code-block:: python
                # Get all packages with a name containing the text 'example package'. Filtering
                # is done on the server side.
                >>> packages = client.packages('example package')
                # Get metadata of the 'example package' package.
                >>> packages['example package'].metadata()

        :return: Prints the metadata.
        """
        utils.print_model_metadata(self)

    def __str__(self):
        separator = "-"*80
        split_description = "\n".join(textwrap.wrap(self.description, 80))
        split_keywords = "\n".join(self.keywords or [])

        # documentation is not guaranteed to be available
        split_documentation = 'No documentation available.'
        if self.documentation is not None:
            split_documentation = "\n".join(textwrap.wrap(self.documentation, 80))

        # When the fields are re-named in the JSON, it breaks our mapping. Use
        #   return str(self.__dict__)
        # to get the new field names then update the below.
        return f"\nPACKAGE \"{self.name}\" " \
               f"(Contains: {self.shape} datasets)\n" \
               f">> ID: {self.id} \n" \
               f">> Accessible: {self.has_access}\n" \
               f"\n" \
               f"{split_description}\n" \
               f"Documentation: {split_documentation}\n\n" \
               f"Keywords:\n{split_keywords}\n" \
               f"{separator}"

    def __repr__(self):
        return f'<Package name={self.name}>'
