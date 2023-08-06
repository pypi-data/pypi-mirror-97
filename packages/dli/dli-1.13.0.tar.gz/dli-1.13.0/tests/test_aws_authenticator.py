import pytest
import time

from dli.boto_authenticator import BotoAuthenticator
from unittest.mock import MagicMock


@pytest.fixture
def tmp_home(monkeypatch, tmpdir):
    # Set the 'home' dir to be a temp dir
    monkeypatch.setenv('HOME', tmpdir)
    yield tmpdir


@pytest.fixture
def client():
    client = MagicMock()
    client._environment.environment_name = 'test'
    client.session.auth_key = 'abc'
    yield client


class TestBotoAuthenticator:

    def test_modifies_existing_creds_file(self, tmp_home, client):
        tmp_home.join('.aws/credentials').ensure()
        tmp_home.join('.aws/credentials').write(
            '[default]\n'
            'aws_access_key_id = other_creds\n'
            'aws_secret_access_key = other_creds\n\n'
        )

        authenticator = BotoAuthenticator(client)
        authenticator.REFRESH_INTERVAL_SECONDS = 0.2

        authenticator.start()
        time.sleep(0.4)

        assert tmp_home.join('.aws/credentials').read() == (
            '[default]\n'
            'aws_access_key_id = other_creds\n'
            'aws_secret_access_key = other_creds\n'
            '\n'
            '[datalake_test]\n'
            'aws_access_key_id = abc\n'
            'aws_secret_access_key = noop\n\n'
        )


    def test_creates_aws_credentials_file(self, tmp_home, client):
        authenticator = BotoAuthenticator(client)
        authenticator.REFRESH_INTERVAL_SECONDS = 0.2

        authenticator.start()
        time.sleep(0.4)

        assert tmp_home.join('.aws/credentials').read() == (
            '[datalake_test]\n'
            'aws_access_key_id = abc\n'
            'aws_secret_access_key = noop\n\n'
        )

    def test_recreates_aws_credentials_file_if_deleted(self, tmp_home, client):
        authenticator = BotoAuthenticator(client)
        authenticator.REFRESH_INTERVAL_SECONDS = 0.2

        authenticator.start()
        time.sleep(0.4)
        assert tmp_home.join('.aws/credentials').exists()
        tmp_home.join('.aws/credentials').remove()
        time.sleep(0.4)
        assert tmp_home.join('.aws/credentials').exists()
