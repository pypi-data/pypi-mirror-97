import operator
import os
import re
from collections import OrderedDict

import boto3
import pytest
from freezegun import freeze_time
from moto import mock_s3

from dli.client.dli_client import DliClient
from datetime import datetime
from unittest.mock import MagicMock


class TestClientMock(DliClient):

    def __init__(self, args, kwargs):
        self._session = MagicMock()
        self._session.auth_key = 'abc'
        self.strict = False
        self._session.token_expires_on = datetime(2100, 1, 1)
        self._environment = MagicMock()
        self._environment.consumption = ''
        self._environment.s3_proxy = 's3proxy.fake'
        self._analytics_handler = MagicMock()
        self.packages = self._packages()
        self.datasets = self._datasets()
        self.logger = MagicMock()

    @property
    def session(self):
        return self._session


@pytest.fixture
def test_client():
    yield TestClientMock('abc', '123')


def mock_catalogue_filter_search_response_impl(body, args, **kwargs):
    # very rudimentary impl of a catalogue parsing the request
    # and responding appropriately given a corpus of packages

    # we're `effectively` testing against a mock here - but otherwise we
    # could only rely on the response of the fixture which we chose
    # or as full-blown integration, so this serves more as a documentation
    # of what catalogue must be doing with our request.

    res = {}
    for x, y in kwargs['params'].items():
        # remove redundant keys
        if x.startswith('filter'):
            try:
                res[re.search(r"\[(\w+)\]\[(\w+)\]", x).groups()] = y
            except Exception as e:
                raise e

    groups = OrderedDict()
    for x in (range(0, int(len(res.keys()) / 3))):
        for key, val in res.items():
            # we'll handle only 0-9 in the tests else this falls down
            if key[0] == str(x):
                if not x in groups:
                    groups[x] = []

                groups[x].append((key[1], val))

    candidates = []
    get_op = {
        "eq": operator.eq,
        "gte": operator.ge,
        "lte": operator.le,
        "gt": operator.gt,
        "lt": operator.lt,
        "like": str.__contains__,
        "ilike": str.__contains__,
        "contains": str.__contains__
    }

    for item in body["data"]:
        passing = True
        for x in list(groups.values()):
            d = dict(x)
            if d['field'] == 'id':
                item_attrib = item.get("id")
            else:
                item_attrib = item["attributes"].get(d['field'])
            like_op = d['operator'] in ['like', 'ilike', 'contain']
            op = get_op[d['operator']]
            if like_op \
                    and not (d['value'].replace("%", "") in item_attrib):
                passing = False
                break
            elif not like_op and not op(item_attrib, d['value']):
                passing = False
                break

        if passing:
            candidates.append(item)

    class Temp():

        def __init__(self, candidates):
            self.candidates = candidates

        def json(self):
            return {'data': self.candidates, 'meta': body["meta"]}

    return Temp(candidates)

@pytest.fixture
def client():
    yield TestClientMock('abc', '123')



@pytest.fixture
def package_request_index_accessible_content_v2():
    return {
        'type': 'package',
        'attributes': {
            'is_internal_within_organisation': True,
            'topic': 'Climate',
            'keywords': [],
            'updated_by': 'api:datalake-mgmt:Timothy.Ryles@ihsmarkit.com',
            'access_manager_id': 'datalake-mgmt',
            'created_by': 'api:datalake-mgmt:Timothy.Ryles@ihsmarkit.com',
            'organisation_name': 'IHS Markit',
            'organisation_id': '9516c0ba-ba7e-11e9-8b34-000c6c0a981f',
            'description': 'test-data',
            'name': 'Test Package',
            'tech_data_ops_id': 'datalake-mgmt',
            'updated_at': '2020-05-13T15:08:07.252878',
            'access': 'Restricted',
            'publisher': 'datalake-mgmt',
            'terms_and_conditions': 'Terms',
            'content_types': ['Reference Data'],
            'has_access': True,
            'taxonomy': ['Data-IHS Markit-Climate'],
            'contract_ids': [],
            'created_at': '2020-05-13T15:08:07.297885',
            'manager_id': 'datalake-mgmt'
        },
        'id': '8d2781c2-952b-11ea-892f-aa2778cbc602'
    }


@pytest.fixture
def package_request_index_unaccessible_content_v2():
    return {
        'type': 'package',
        'attributes': {
            'is_internal_within_organisation': True,
            'topic': 'Finance',
            'keywords': [],
            'updated_by': 'api:datalake-mgmt:Timothy.Ryles@ihsmarkit.com',
            'access_manager_id': 'datalake-mgmt',
            'created_by': 'api:datalake-mgmt:Timothy.Ryles@ihsmarkit.com',
            'organisation_name': 'Test Org',
            'organisation_id': '9516c0ba-ba7e-11e9-8b34-000c6c0a981f',
            'description': 'test-data',
            'name': 'Different Name',
            'tech_data_ops_id': 'datalake-mgmt',
            'updated_at': '2020-05-13T15:08:07.252878',
            'access': 'Restricted',
            'publisher': 'datalake-mgmt',
            'terms_and_conditions': 'Terms',
            'content_types': ['Reference Data'],
            'has_access': False,
            'taxonomy': ['Data-Test Org-Finance'],
            'contract_ids': [],
            'created_at': '2020-05-13T15:08:07.297885',
            'manager_id': 'datalake-mgmt'
        },
        'id': '8d2781c2-952b-11ea-892f-aa2778cbc602'
    }


@pytest.fixture
def package_request_index_v2(package_request_index_accessible_content_v2,
                             package_request_index_unaccessible_content_v2):
    return {
        'data': [package_request_index_accessible_content_v2, package_request_index_unaccessible_content_v2],
        'meta': {
           'total_count': 2, 'page': 1, 'page_size': 5000, 'total_pages': 1
        }
    }


@pytest.fixture
def dataset_request_index_accessible_content_v2():
    return {
        'type': 'dataset',
         'attributes': {
             'package_id': '59e6a698-975d-11e9-84cc-7e5ef76d533f',
             'updated_by': 'update@ihsmarkit.com',
             'keywords': [],
             'location': {},
             'content_type': 'Structured',
             'has_access': True,
             'first_datafile_at': '2019-05-06',
             'short_code': 'TestDataset',
             'absolute_taxonomy': 'Data-Test',
             'publishing_frequency': 'Monthly',
             'name': 'Test DataSet',
             'last_datafile_at': '2020-01-01',
             'data_format': 'PARQUET',
             'created_at': '2019-06-25',
             'description': 'description',
             'organisation_name': 'IHS Markit',
             'created_by': 'creator@ihsmarkit.com',
             'taxonomy': []
         },
         'id': '5b01376e-975d-11e9-8832-7e5ef76d533f'
    }


@pytest.fixture
def dataset_request_index_unaccessible_content_v2():
    return {
        'type': 'dataset',
         'attributes': {
             'package_id': '59e6a698-975d-11e9-84cc-0000000000',
             'updated_by': 'update@ihsmarkit.com',
             'keywords': [],
             'location': {},
             'content_type': 'Structured',
             'has_access': False,
             'first_datafile_at': '2019-05-06',
             'short_code': 'OtherDataset',
             'absolute_taxonomy': 'Data-Test',
             'publishing_frequency': 'Monthly',
             'name': 'Other DataSet',
             'last_datafile_at': '2020-01-01',
             'data_format': 'PARQUET',
             'created_at': '2019-06-25',
             'description': 'description',
             'organisation_name': 'IHS Markit',
             'created_by': 'creator@ihsmarkit.com',
             'taxonomy': []
         },
         'id': '5b01376e-975d-11e9-8832-7e5ef76d533f'
    }


@pytest.fixture
def dataset_request_index_v2(dataset_request_index_accessible_content_v2,
                             dataset_request_index_unaccessible_content_v2):
    return {
            'data':
                [dataset_request_index_accessible_content_v2,
                 dataset_request_index_unaccessible_content_v2
                ],
            'meta': {'total_count': 2, 'page': 1,
                     'total_pages': 1}
          }


@pytest.fixture
def package_request_v2():
    return {
        'data': {
            'id': '1234',
            'attributes': {
                'name': 'Test Package',
                'topic': 'Test Topic',
                'keywords': ['test'],
                'hasAccess': True,
                'description': 'DESC',
                'documentation': 'href',
            }
        }
    }


@pytest.fixture
def dataset_request_v2():
    return {
            'data': {
                'type': 'dataset',
                'attributes': {
                     'package_id': '59e6a698-975d-11e9-84cc-7e5ef76d533f',
                     'updated_by': 'update@ihsmarkit.com',
                     'keywords': [],
                     'location': {},
                     'content_type': 'Structured',
                     'has_access': False,
                     'first_datafile_at': '2019-05-06',
                     'short_code': 'TestDataset',
                     'absolute_taxonomy': 'Data-Test',
                     'publishing_frequency': 'Monthly',
                     'name': 'Test DataSet',
                     'last_datafile_at': '2020-01-01',
                     'data_format': 'PARQUET',
                     'created_at': '2019-06-25',
                     'description': 'description',
                     'organisation_name': 'IHS Markit',
                     'created_by': 'creator@ihsmarkit.com',
                     'taxonomy': []
                 },
             'id': '5b01376e-975d-11e9-8832-7e5ef76d533f'
        }
      }


@pytest.fixture
def visible_orgs_v2():
    return {
        'data': [{
            'attributes': {
                'external_company_id': '47cbc80a-d9ad-4aeb-9263-10646b6c9a8e',
                'created_by': 'tim@ihsmarkit.com',
                'description': None,
                'is_visible': True,
                'name': 'testorg',
                'short_code': 'karolinatestorgR9QZ',
                'created_on': '2020-06-02T09:06:03.473793+00:00',
                'updated_by': 'Karolina.Olszewska@ihsmarkit.com',
                'updated_on': '2020-06-02T09:06:03.473793+00:00',
                'domains': [{'domain_name': 'karolina.test'}]
            },
           'id': 'e3546799-db0f-48c4-81a3-b1b62669f05a'
        }]
    }



@pytest.fixture
def instance_request_v1():
    return {
        'properties': {'pages_count': 1},
        'entities': [{
            'properties': {'datafileId': 1,  'total_size': 1048576}
        }]
    }


@pytest.fixture
def dictionary_request_v2():
    return {
        'data': {
        'type': 'dictionary',
        'attributes': {
          'dataset_id': '7eb6eb49-5fae-44bc-900a-c241e0a24b00',
          'description': None,
          'version': '1',
          'partitions': [],
          'valid_as_of': '2019-09-26'
        },
        'id': '2d113c3a-be1a-4c70-b87a-8e569dee8dd0'}
    }


@pytest.fixture
def fields_request_v2():
    return {
        'data':
        {
            'type': 'dictionary_fields',
            'attributes': {
                  'fields': [
                    {'nullable': True,
                     'type': 'String',
                     'description': 'IHS',
                     'name': 'col1'},
                    {'nullable': True,
                     'type': 'String',
                     'description': 'IHS',
                     'name': 'col2'},
                    {'nullable': False,
                     'type': 'String',
                     'description': 'IHS',
                     'name': 'col3'},
                  ]
            },
            'id': '2d113c3a-be1a-4c70-b87a-8e569dee8dd0'
        },
        'meta': {'total_count': 3}
    }

@pytest.fixture
def unstructured_dataset_request_v2():
    return {
            'data': {
                'type': 'dataset',
                'attributes': {
                     'package_id': '59e6a698-975d-11e9-84cc-7e5ef76d533f',
                     'updated_by': 'update@ihsmarkit.com',
                     'keywords': [],
                     'location': {},
                     'content_type': 'Unstructured',
                     'has_access': False,
                     'first_datafile_at': '2019-05-06',
                     'short_code': 'TestDataset',
                     'absolute_taxonomy': 'Data-Test',
                     'publishing_frequency': 'Monthly',
                     'name': 'Test DataSet',
                     'last_datafile_at': '2020-01-01',
                     'data_format': 'PARQUET',
                     'created_at': '2019-06-25',
                     'description': 'description',
                     'organisation_name': 'IHS Markit',
                     'created_by': 'creator@ihsmarkit.com',
                     'taxonomy': []
                 },
             'id': '5b01376e-975d-11e9-8832-7e5ef76d533f'
        }
      }


@pytest.fixture
def unstructured_dataset_request_index_accessible_content_v2():
    return {
        'type': 'dataset',
         'attributes': {
             'package_id': '59e6a698-975d-11e9-84cc-7e5ef76d533f',
             'updated_by': 'update@ihsmarkit.com',
             'keywords': [],
             'location': {},
             'content_type': 'Unstructured',
             'has_access': True,
             'first_datafile_at': '2019-05-06',
             'short_code': 'TestDataset',
             'absolute_taxonomy': 'Data-Test',
             'publishing_frequency': 'Monthly',
             'name': 'Test DataSet',
             'last_datafile_at': '2020-01-01',
             'data_format': 'PARQUET',
             'created_at': '2019-06-25',
             'description': 'description',
             'organisation_name': 'IHS Markit',
             'created_by': 'creator@ihsmarkit.com',
             'taxonomy': []
         },
         'id': '5b01376e-975d-11e9-8832-7e5ef76d533f'
    }


@pytest.fixture
def aws_s3():
    """Set up Mock S3"""
    with mock_s3() as s3:
        yield s3

@pytest.fixture
def object_summaries_s3(aws_s3, request):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
        'resources', 's3_listings'))

    with freeze_time('2020-01-01T00:00:00Z'):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket')

        for root, dirs, files in os.walk(path):
            for file in files:
                with open(os.path.join(root, file), 'rb') as f:
                    file_data = f.read()

                s3_resource.Object('bucket',
                   f'abc/{root.replace(path + "/", "")}/{file}').put(
                    Body=file_data
                )

    yield [f for f in bucket.objects.all()]

@pytest.fixture
def unstructured_object_summaries_s3(aws_s3, request):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
        'resources', 's3_unstructured_listings'))

    with freeze_time('2020-01-01T00:00:00Z'):
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket='bucket')

        for root, dirs, files in os.walk(path):
            for file in files:
                with open(os.path.join(root, file), 'rb') as f:
                    file_data = f.read()

                s3_resource.Object('bucket',
                   f'abc/{root.replace(path + "/", "")}/{file}').put(
                    Body=file_data
                )

    yield [f for f in bucket.objects.all()]


@pytest.fixture
def unstructured_dataset_request_index_v2(unstructured_dataset_request_index_accessible_content_v2,
                                          dataset_request_index_unaccessible_content_v2):
    return {
        'data': [
            unstructured_dataset_request_index_accessible_content_v2,
            dataset_request_index_unaccessible_content_v2
        ],
        'meta': {
            'total_count': 2,
            'page': 1,
            'total_pages': 1
        }
    }