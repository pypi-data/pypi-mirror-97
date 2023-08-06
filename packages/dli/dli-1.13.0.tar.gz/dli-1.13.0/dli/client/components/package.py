#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
import warnings

import requests

from dli.client.components.urls import package_urls
from dli.client.components import SirenComponent, SirenAdapterResponse
from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.client.utils import filter_out_unknown_keys, to_camel_cased_dict

logger = logging.getLogger(__name__)


class Package(SirenComponent):

    _KNOWN_FIELDS = {"name",
                     "description",
                     "keywords",
                     "topic",
                     "access",
                     "internalData",
                     "contractIds",
                     "termsAndConditions",
                     "derivedDataNotes",
                     "derivedDataRights",
                     "distributionNotes",
                     "distributionRights",
                     "internalUsageNotes",
                     "internalUsageRights",
                     "documentation",
                     "publisher",
                     "techDataOpsId",
                     "accessManagerId",
                     "managerId",
                     "intendedPurpose",
                     "isInternalWithinOrganisation"}
    """
    A mixin providing common package operations
    """

    def get_package(self, id=None, name=None):
        """
        Fetches package metadata for an existing package.

        :param str id: The id of the package.
        :param str name: The name of the package. We will perform a case
        sensitive exact match on this name in the database. If you want
        a non-exact match or a case insensitive match, then please consider
        using the `packages` call instead with the `search_term` parameter
        and an `ilike` matcher, for example:

        .. code:: python

            client.packages(search_term='name ilike example')

        :returns: A package instance
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # Look up by package id
                package = client.get_package('my_package_id')
                # or
                package = client.get_package(id='my_package_id')

                # Alternatively look up by package name
                package = client.get_package(name='my_package')

        """

        warnings.warn(
            'This method is deprecated and is scheduled for removal in '
            'dli==1.14.0. '
            '\nTo search for a package, please use this call instead:'
            '\n'
            '\n    import dli'
            '\n    client = dli.connect()'
            '\n    # Return type: OrderedDict[str, PackageModel]'
            '\n    packages = client.packages(search_term=["name=<package_name>"])',
            PendingDeprecationWarning
        )

        if id is None and name is None:
            raise ValueError("Either package id or name must be specified to look up package")

        return self._get_package(package_id=id, name=name)

    def get_package_datasets(self, package_id, count=100):
        """
        Returns a list of all datasets registered under a package.

        :param str package_id: The id of the package.
        :param int count: Optional. Count of datasets to be returned. Defaults to 100.

        :returns: List of all datasets registered under the package.
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                datasets = client.get_package_datasets(
                    package_id,
                    count=100
                )
        """
        response = self.session.get(
            package_urls.v2_package_datasets.format(id=package_id),
            params={'page_size': count}
        )

        return self._DatasetFactory._from_v2_list_response(response.json())

    @staticmethod
    def get_default_package_terms_and_conditions(organisation_name: str):
        """
        Returns a string representing the default Terms And Conditions for packages created in DataLake.

        :returns: The default DataLake Terms And Conditions
        :rtype: str
        """
        if organisation_name == 'IHS Markit':
            return ('By submitting this Data request and checking the "Accept Terms and Conditions" '
                'box, you acknowledge and agree to the following:\n'
                '\n'
                '* To promptly notify the relevant Access Manager/Producer of your intended use '
                'of the Data;\n'
                '* To obtain the terms and conditions relevant to such use for such Data from '
                'the Producer;\n'
                '* To distribute such terms and conditions to each member of your '
                'Consumer Group who may use the Data;\n'
                '* To use the Data solely for such intended use, subject to such terms and '
                'conditions;\n'
                '* To ensure that the Data is only accessed by members of your Consumer Group, '
                'and only used by such members for such intended use, subject to such terms and '
                'conditions;\n'
                '* To adhere to any additional requests of Producer with respect to the Data '
                '(including but not limited to ceasing use of the Data and deleting the Data, '
                'and ensuring other members of the Consumer Group do so, upon revocation of your '
                'license by Producer).\n'
                '\n'
                'Please refer to the <a href="/terms-of-use" target="_blank">EULA</a> for any '
                'defined terms used above. '
                'The <a href="/terms-of-use" target="_blank">EULA</a> '
                'is the document you agreed to adhere to by accessing the Lake.')
        else:
            return ''

    #
    # Private functions
    #
    def _get_package(self, **kwargs):
        vals = []

        if 'package_id' in kwargs and kwargs['package_id'] is not None:
            vals = self.packages(
                search_term=[f"id={kwargs['package_id']}"]).values()

        elif 'name' in kwargs and kwargs['name'] is not None:
            vals = self.packages(
                search_term=[f"name={kwargs['name']}"]).values()

        else:
            raise ValueError("Either package id or name must be specified to look up package")

        vals = list(vals)

        if len(vals) == 1:
            if hasattr(vals[0], "id"):
                # Add an alias of the `id` attribute named `package_id`.
                vals[0].package_id = vals[0].id

            return vals[0]
        elif len(vals) < 1:
            r = requests.Response()
            r.status_code = 404
            r.request = (lambda: True)
            r.request.method = f"Package {kwargs['package_id'] if kwargs.get('package_id') else kwargs['name']}"
            r.request.url = ""
            raise CatalogueEntityNotFoundException(
                message=f"Package "
                f"{kwargs['package_id'] if kwargs.get('package_id') else kwargs['name']}",
                response=r
            )
        else:
            return vals

    @staticmethod
    def _validate_fields(fields):
        if 'termsAndConditions' in fields:
            Package._validate_terms_and_conditions(fields.get("termsAndConditions"))

    @staticmethod
    def _validate_terms_and_conditions(field):
        if not field or not field.strip():
            raise ValueError("Terms and conditions must be defined "
                             "and be non empty, non blank string")
