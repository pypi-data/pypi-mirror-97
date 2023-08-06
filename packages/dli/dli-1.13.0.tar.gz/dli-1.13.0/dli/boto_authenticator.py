import threading
import time
import sys
import os
import configparser


class BotoAuthenticator(threading.Thread):

    # As long as this is less than the margin on error between
    # the session.has_expired and the real time the credentials
    # should always be updated
    REFRESH_INTERVAL_SECONDS = 20

    def __init__(self, client):
        super().__init__()
        self.daemon = True
        self._client = client
        self._exit_flag = threading.Event()
        self.profile_name = (
            f'datalake_{self._client._environment.environment_name}'
        )
        print(
            f'Authenticator started. This will run until the DLI is closed'
            f'. This maintains up to date credentials '
            f'in your ~/.aws/credentials file under the profile '
            f'{self.profile_name}.\n'
            f'\nThis tool supports the following:\n\n'
            f'\t+--------------+-------------------------+\n'
            f'\t| Library/Tool |    Version Supported    |\n'
            f'\t+--------------+-------------------------+\n'
            f'\t| Boto3        | Any Released After 2014 |\n'
            f'\t| sdk-for-ruby | Any Released After 2014 |\n'
            f'\t| AWS-Java-SDK | 1.7.8 - 2014            |\n'
            f'\t| C++ AWS SDK  | Recent Versions         |\n'
            f'\t| Cyberduck    | Coming soon             |\n'
            f'\t| s5cmd        | All Versions            |\n'
            f'\t| Dask         | All Versions            |\n'
            f'\t| awscli       | All Versions            |\n'
            f'\t+--------------+-------------------------+\n'
        )

    def run(self):
        while True:
            try:
                self._authenticate()
                should_exit = self._exit_flag.wait(
                    timeout=self.REFRESH_INTERVAL_SECONDS
                )

                if should_exit:
                    break
            except Exception as e:
                self._client.logger.exception(
                    'Could not update credentials: ', e
                )
                break

    def stop(self):
        self._exit_flag.set()
        self._client.logger.info('Stopping Authenticator')

    def _authenticate(self):
        # This is a property lookup - so may call
        # if the session is expired.
        auth_key = self._client.session.auth_key
        shared_credentials = os.path.expanduser('~/.aws/credentials')

        # If the ~/.aws dir doesn't exists we create it
        os.makedirs(os.path.dirname(shared_credentials), exist_ok=True)

        config = configparser.ConfigParser()
        config.read(shared_credentials)

        written_access_key_id = None

        try:
            written_access_key_id = config.get(
                self.profile_name, 'aws_access_key_id'
            )
        except configparser.NoSectionError:
            pass

        # If what's on disk differs, update it
        if written_access_key_id != self._client.session.auth_key:
            self._client.logger.info(
                'Writing authentication info To ~/.aws/credentials'
            )

            config[self.profile_name] = {
                'aws_access_key_id': self._client.session.auth_key,
                'aws_secret_access_key': 'noop',
            }

            with open(shared_credentials, 'w') as configfile:
                config.write(configfile)
        else:
            self._client.logger.debug(
                'Up to date ~/.aws/credentials'
            )
