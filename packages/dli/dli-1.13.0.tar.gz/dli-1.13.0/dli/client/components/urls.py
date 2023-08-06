#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import urllib


class dataset_urls:
    # instance = '/__api/datasets/{id}/'
    # index = '/__api/datasets/'
    datafiles = '/__api/datasets/{id}/datafiles/'
    latest_datafile = '/__api/datasets/{id}/latest-datafile/'
    # keys = '/__api/datasets/{id}/keys/'
    access_keys = '/__api/request-access-keys/'

    # dli_v2
    v2_index = '/__api_v2/datasets/'
    v2_by_id = '/__api_v2/datasets/{id}/'
    v2_by_short_code = '/__api_v2/by_short_code/dataset/{dataset_short_code}'
    v2_sample_data_schema = '/__api_v2/datasets/{id}/sample_data'
    v2_sample_data_file = '/__api_v2/datasets/{id}/sample_data/file'
    v2_schema_instance_version = '/__api_v2/datasets/{id}/dictionaries/{version}'
    v2_unstructured_document = '/__api_v2/datasets/{id}/documents'

    # schemas_many = '/__api/datasets/{id}/schemas/'
    # schema_instance = '/__api/datasets/{id}/schema/'

    dictionary_index =  '/__api_v2/dictionaries/'
    dictionary_instance = '/__api_v2/dictionaries/{id}/'
    dictionary_by_dataset = '/__api_v2/datasets/{id}/dictionaries/'
    dictionary_by_dataset_lastest = '/__api_v2/datasets/{id}/current_dictionary/'
    dictionary_fields = '/__api_v2/dictionaries/{id}/fields/'


class autoreg_urls:
    autoreg_index = '/__api/auto-reg-metadata/'
    autoreg_instance = '/__api/auto-reg-metadata/{id}/'


class datafile_urls:
    datafiles_index = '/__api/datafiles/'
    datafiles_instance = '/__api/datafiles/{id}/'


class me_urls:
    # '/__api_v2/me/managed_packages'  # Will be changing the endpoint below to the V2 URL
    # in DLI==1.13.0b3 after Catalogue release 1.40 to Prod.
    my_packages = '/__api/me/my-packages/'
    my_accounts = '/__api/me/my_accounts/'


class package_urls:
    package_index = '/__api/packages/'
    package_edit = '/__api/packages/{id}/'
    # package_datasets = '/__api/package/{id}/datasets/'

    # dli_v2
    v2_package_datasets = '/__api_v2/packages/{id}/datasets'
    v2_package_by_id = '/__api_v2/packages/{id}'
    v2_package_index = '/__api_v2/packages'


class search_urls:
    search_root = '/__api/search/'
    search_packages = '/__api/search/packages/'
    search_datasets = '/__api/search/datasets/'


class consumption_urls:
    consumption_download = '/datafile/{id}/download/binary/{path}'
    consumption_manifest = '/datafile/{id}/manifest/'
    consumption_dataframe = '/dataset/{id}/dataframe/'
    consumption_analytics = '/analytics/'
    consumption_partitions = '/dataset/{id}/partitions/'


# class accounts_urls:
#     account_instance = '/__api/account/{id}/'

class sam_urls:
    sam_token = '/sso/oauth2/realms/root/realms/Customers/access_token'

class identity_urls:
    identity_token = '/api/identity/v2/auth/token'
    identity_postbox = '/api/identity/v1/postbox_login'
    identity_poll = '/api/identity/v2/auth/postbox'
    org_by_id = '/api/identity/v2/organisations/{id}'
    orgs_visible_to_user = '/api/identity/v2/organisations/visible'