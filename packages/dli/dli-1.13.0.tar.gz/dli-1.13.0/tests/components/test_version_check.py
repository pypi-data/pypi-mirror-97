from unittest.mock import MagicMock, patch
from dli.client import session as sm


class TestVersionCheck:

    def test_ssl_error_in_version_check_caught(self):
        # going to same server as pypi but not with a valid hostname.
        with patch('dli.client.session.trace_logger') as logger_mock:
            sm._set_pypi_url = MagicMock(
                return_value='https://151.101.60.223/pypi/dli/json'
            )
            sm.version_check(package_name='dli')
            logger_mock.warning.assert_called()
