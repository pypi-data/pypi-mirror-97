#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
from urllib.parse import urlparse, ParseResult


class _Environment:

    _catalogue_environment_name_map = {
        'catalogue.datalake.ihsmarkit.com': 'prod',
        'catalogue-testprod.datalake.ihsmarkit.com': 'testprod',
        'catalogue-uat.datalake.ihsmarkit.com': 'uat',
        'client-uat.datalake.ihsmarkit.com': 'uat2',
        'catalogue-dev.udpmarkit.net': 'dev',
        'catalogue-qa.udpmarkit.net': 'qa',
        'catalogue-qa2.udpmarkit.net': 'qa2',
        'catalogue-qa3.udpmarkit.net': 'qa3',
    }

    _catalogue_accounts_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 'catalogue.datalake.ihsmarkit.com',
        'catalogue-testprod.datalake.ihsmarkit.com': 'catalogue-testprod.datalake.ihsmarkit.com',
        'catalogue-uat.datalake.ihsmarkit.com': 'catalogue-uat.datalake.ihsmarkit.com',
        'client-uat.datalake.ihsmarkit.com': 'client-uat.datalake.ihsmarkit.com',
        'catalogue-dev.udpmarkit.net': 'catalogue-dev.udpmarkit.net',
        'catalogue-qa.udpmarkit.net': 'catalogue-qa.udpmarkit.net',
        'catalogue-qa2.udpmarkit.net': 'catalogue-qa2.udpmarkit.net',
        'catalogue-qa3.udpmarkit.net': 'catalogue-qa3.udpmarkit.net',
    }

    _catalogue_consumption_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 'consumption.datalake.ihsmarkit.com',
        'catalogue-testprod.datalake.ihsmarkit.com': 'consumption-testprod.datalake.ihsmarkit.com',
        'catalogue-uat.datalake.ihsmarkit.com': 'consumption-uat.datalake.ihsmarkit.com',
        'client-uat.datalake.ihsmarkit.com': 'consumption-uat2.datalake.ihsmarkit.com',
        'catalogue-dev.udpmarkit.net': 'consumption-dev.udpmarkit.net',
        'catalogue-qa.udpmarkit.net': 'consumption-qa.udpmarkit.net',
        'catalogue-qa2.udpmarkit.net': 'consumption-qa2.udpmarkit.net',
        'catalogue-qa3.udpmarkit.net': 'consumption-qa3.udpmarkit.net',
    }

    _catalogue_sam_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 'sam.ihsmarkit.com',
        'catalogue-testprod.datalake.ihsmarkit.com': 'sam.ihsmarkit.com',
        'catalogue-uat.datalake.ihsmarkit.com': 'sam.ihsmarkit.com',
        'client-uat.datalake.ihsmarkit.com': 'sam.ihsmarkit.com',
        'catalogue-qa.udpmarkit.net': 'sam.samexternal.net',
        'catalogue-qa2.udpmarkit.net': 'sam.samexternal.net',
        'catalogue-qa3.udpmarkit.net': 'sam.samexternal.net',
        'catalogue-dev.udpmarkit.net': 'sam.samexternal.net',
    }

    _catalogue_sam_client_map = {
        'catalogue.datalake.ihsmarkit.com': 'datalake-pkce-prod-q56PXZSTDQ',
        'catalogue-testprod.datalake.ihsmarkit.com': 'datalake-pkce-prod-q56PXZSTDQ',
        'catalogue-uat.datalake.ihsmarkit.com': 'datalake-pkce-uat-RMrWmjPhql',
        'client-uat.datalake.ihsmarkit.com': 'datalake-pkce-uat-RMrWmjPhql',
        'catalogue-qa.udpmarkit.net': 'datalake-pkce-sqa-BSFwJUigI4',
        'catalogue-qa2.udpmarkit.net': 'datalake-pkce-sqa-BSFwJUigI4',
        'catalogue-qa3.udpmarkit.net': 'datalake-pkce-sqa-BSFwJUigI4',
        'catalogue-dev.udpmarkit.net': 'datalake-pkce-dev-sS8hXQiT2m',
    }

    _s3_proxy_environment_map = {
        'catalogue.datalake.ihsmarkit.com': 's3.datalake.ihsmarkit.com',
        'catalogue-testprod.datalake.ihsmarkit.com': 's3-testprod.datalake.ihsmarkit.com',
        'catalogue-uat.datalake.ihsmarkit.com': 's3-uat.datalake.ihsmarkit.com',
        'client-uat.datalake.ihsmarkit.com': 's3-uat2.datalake.ihsmarkit.com',
        'catalogue-qa.udpmarkit.net': 's3-qa.udpmarkit.net',
        'catalogue-qa2.udpmarkit.net': 's3-qa2.udpmarkit.net',
        'catalogue-qa3.udpmarkit.net': 's3-qa3.udpmarkit.net',
        'catalogue-dev.udpmarkit.net': 's3-dev.udpmarkit.net',
    }

    def __init__(self, api_root):
        """
        Class to manage the different endpoints

        :param str root_url: The root url of the catalogue
        """

        catalogue_parse_result = urlparse(api_root)

        self.catalogue = ParseResult(
            catalogue_parse_result.scheme, catalogue_parse_result.netloc,
            '', '', '', ''
        ).geturl()

        accounts_host = self._catalogue_accounts_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.accounts = ParseResult(
            catalogue_parse_result.scheme, accounts_host, '', '', '', ''
        ).geturl()

        consumption_host = self._catalogue_consumption_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.consumption = ParseResult(
            'https', consumption_host, '', '', '', ''
        ).geturl()

        sam_host = self._catalogue_sam_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.sam = ParseResult(
            'https', sam_host, '', '', '', ''
        ).geturl()

        self.sam_client = self._catalogue_sam_client_map.get(
            catalogue_parse_result.netloc
        )

        self.s3_proxy = self._s3_proxy_environment_map.get(
            catalogue_parse_result.netloc
        )

        self.environment_name = self._catalogue_environment_name_map.get(
            catalogue_parse_result.netloc, 'unknown'
        )
