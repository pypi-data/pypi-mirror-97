import json
import os
import random
import string
import time
import unittest
import uuid
import jwt
from unittest.mock import patch

import requests
from urllib import parse

from dli.client import builders, session
from tests import localstack_helper

token_data = {
  "aud": "datalake-catalogue-dev",
  "auth_time": 1513331509,
  "datalake": {
    "accounts": {
      "iboxx": "rw",
      "mrd": "r",
      "datalake-mgmt": "rw"
    },
    "tenant_id": "4e27686c-e72a-44f1-a126-f0d2940617d4",
    "organisation_id": "4e27686c-e72a-44f1-a126-f0d2940617d4",
    "user_id": "4e27686c-e72a-44f1-a126-f0d2940617d4",
  },
  "email": "jim@example.com",
  "email_verified": True,
  "exp": 9513335109,
  "iat": 1513331509,
  "iss": "https://hydra-dev.udpmarkit.net",
  "nonce": "5a823264-b7d3-485e-b761-ec1512944814",
  "sub": "user:12345:jim"
}


def _get_token(payload, secret: str) -> str:
    token_encoded = jwt.encode(payload, secret)
    if isinstance(token_encoded, bytes):
        return token_encoded.decode('utf-8')
    else:
        return token_encoded


token = _get_token(token_data, 'secret')


class SdkIntegrationTestCase(unittest.TestCase):
    """
    Helper TestCase to test against a local docker container running the datacat api.
    To run these locally, run `docker-compose up` on the root directory
    """

    aws_account_id = "12345"

    @patch("dli.client.dli_client.Session._get_auth_key", lambda self: token)
    @patch("dli.client.dli_client.AnalyticsHandler", lambda self: None)
    def setUp(self):
        self.headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(token),
            'Cookie': 'oidc_id_token=' + token
        }
        self.root_url = os.environ.get(
            "DATA_LAKE_INTERFACE_URL", "http://data-lake-interface:8080/__api/")
        self.api_key = self.get_api_key()
        self.client = self.create_session()
        self.s3 = []

        while True:
            try:
                #keep sleeping until we can actually register.
                time.sleep(1)
                self.register_aws_account(self.aws_account_id)
                break
            except:
                continue

        self.s3_client = localstack_helper.get_s3_client()

    def patch_upload_files_to_s3(self, files, location, tr=None, r=None):
        result = []
        for f in files:
            path = location + os.path.basename(f)
            self.s3.append(path)
            result.append({"path": "s3://" + path})
        return result

    def get_api_key(self):
        # url = "%s/generate-my-key" % self.root_url
        # payload = {
        #     "account": "datalake-mgmt",
        #     "rights": "rw",
        #     "expiration": "2030-01-01"
        # }

        # response = requests.post(url, data=json.dumps(payload), headers=self.headers)
        # return response.text
        return "key"

    def create_package(self, name, access="Restricted", **kwargs):
        payload = {
            "name": name + "_" + str(uuid.uuid4()),
            "description":  "asd",
            "publisher":  "datalake-mgmt",
            "manager_id":  "datalake-mgmt",
            "access_manager_id":  "datalake-mgmt",
            "tech_data_ops_id":  "datalake-mgmt",
            "topic":  "Climate",
            "access":  access,
            "internal_data":  "No",
            "terms_and_conditions":  "Terms and Conditions"
        }
        payload.update(**kwargs)
        return self.client.register_package(**payload).id

    def dataset_builder(self, package_id, dataset_name, **kwargs):
        arguments = dict(kwargs)
        data_preview_type = arguments.pop('data_preview_type', 'NONE')
        default_short_code = ''.join(random.choices(
            string.ascii_letters + string.digits, k=10
        ))
        short_code = arguments.pop('short_code', default_short_code)
        return builders.DatasetBuilder(
            package_id=package_id,
            name=dataset_name,
            description='a testing dataset',
            content_type='Structured',
            data_format='CSV',
            publishing_frequency='Daily',
            taxonomy=[],
            data_preview_type=data_preview_type,
            short_code=short_code,
            **arguments
        )

    def register_s3_dataset(self, package_id, dataset_name, bucket_name, prefix="prefix"):
        self._setup_bucket_and_prefix(bucket_name, prefix)
        return self.client.register_dataset(
            self.dataset_builder(package_id, dataset_name).with_external_s3_storage(
                bucket_name,
                self.aws_account_id,
                prefix
            )
        )

    def _setup_bucket_and_prefix(self, bucket_name, prefix):
        # API checks whether DataLake can access S3 bucket at prefix. If dataset is registered with S3 location
        # we must create a fake one in localstack.
        s3_client = self.s3_client
        s3_client.create_bucket(Bucket=bucket_name)
        s3_client.put_object(
            Bucket=bucket_name,
            # Ensure key ends in a slash to signify it's a directory
            Key=prefix.rstrip('/') + '/',
            Body=""
        )

        def cleanup_bucket():
            for object_to_delete in s3_client.list_objects(Bucket=bucket_name)['Contents']:
                s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": [{"Key": object_to_delete['Key']}]})
            s3_client.delete_bucket(Bucket=bucket_name)

        self.addCleanup(cleanup_bucket)


    def create_session(self):
        return session._start_session(self.api_key, self.root_url)

    def register_aws_account(self, aws_account_id):
        response = requests.post(
            parse.urljoin(self.root_url, "me/aws-accounts"),
            headers=self.headers,
            data=json.dumps({
                "awsAccountId": str(aws_account_id),
                "awsAccountName": str(aws_account_id),
                "awsRegion": "eu-west-1",
                "accountIds": ["datalake-mgmt"],
                "awsRoleArn": 'arn:aws:iam::000000000001:user/root'
            })
        )

        self.assertEqual(response.status_code, 200)

    def assert_page_count_is_valid_for_paginated_resource_actions(self, func):
        with self.assertRaises(ValueError):
            func(-1)
        with self.assertRaises(ValueError):
            func(0)
        with self.assertRaises(ValueError):
            func("test")


def eventually(assertion, delay=1, retries=5):
    try:
        return assertion()
    except Exception as e:
        if retries <= 1:
            raise e
        time.sleep(delay)
        return eventually(assertion, delay=delay, retries=retries-1)
