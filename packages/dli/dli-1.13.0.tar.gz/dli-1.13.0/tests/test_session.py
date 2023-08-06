import json
import os
import time
from urllib.parse import urlencode

import keyring
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import pytest
import unittest
import jwt
from unittest.mock import MagicMock, patch, Mock
import httpretty

from dli import __version__, __product__
from dli.client.components.urls import identity_urls
from dli.client.dli_client import Session, DliClient
from dli.client.environments import _Environment
from dli.client.session import _start_session
from dli.client import session
from dli.client.exceptions import (
    DatalakeException,
    InsufficientPrivilegesException,
    UnAuthorisedAccessException
)
from dli.siren import PatchedSirenBuilder

environ = MagicMock(catalogue='http://catalogue.local',
                    accounts='')


def _get_token(payload, secret: str) -> str:
    token_encoded = jwt.encode(payload, secret)
    if isinstance(token_encoded, bytes):
        return token_encoded.decode('utf-8')
    else:
        return token_encoded


valid_token: str = _get_token({"exp": 9999999999}, 'secret')
expired_token: str = _get_token({"exp": 1111111111}, 'secret')
long_token: str = _get_token({"exp": 9999999999, "accounts": ["test"]*1000}, 'secret')


class SessionTestCase(unittest.TestCase):

    def test_can_decode_valid_jwt_token(self):
        ctx = Session(
            access_id=None,
            secret_key="key",
            environment=environ,
            host=None,
            auth_key=valid_token,
            logger=MagicMock()
        )

        self.assertFalse(ctx.has_expired)

    def test_can_detect_token_is_expired(self):
        ctx = Session(
            access_id=None,
            secret_key="key",
            environment=environ,
            host=None,
            auth_key=expired_token,
            logger=MagicMock()
        )
        self.assertTrue(ctx.has_expired)


class SessionRequestFactoryTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def session(self):
        self.session = Session(
            access_id=None, secret_key=None, environment=environ,
            host=None,
            auth_key=valid_token,
            logger=MagicMock()
        )

    @httpretty.activate
    def test_response_403_raises_InsufficientPrivilegesException(self):
        response_text = 'Insufficient Privileges'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=403, body=response_text
        )

        with self.assertRaises(InsufficientPrivilegesException):
            self.session.get('/test')

    @httpretty.activate
    def test_response_401_raises_UnAuthorisedAccessException(self):
        response_text = 'UnAuthorised Access'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=401, body=response_text
        )


        with self.assertRaises(UnAuthorisedAccessException):
            self.session.get('/test')

    @httpretty.activate
    def test_response_500_raises_DatalakeException(self):
        response_text = 'Datalake server error'
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/test',
            status=500, body=response_text
        )

        with self.assertRaises(DatalakeException):
            self.session.get('/test')

    @httpretty.activate
    def test_sdk_version_is_included_in_header(self):
        httpretty.register_uri(
            httpretty.GET, 'http://catalogue.local/__api/',
            status=200, body="response"
        )
        # issue a request
        self.session.get('/__api/')

        request = httpretty.last_request()
        self.assertTrue("X-Data-Lake-SDK-Version" in request.headers)
        self.assertEqual(request.headers["X-Data-Lake-SDK-Version"], str(__version__))


class UnitTestSessionMock(Session):

    def __init__(self, id, pasw):
        self._get_SAM_auth_key = MagicMock()
        self._get_auth_key = MagicMock()
        self._get_decoded_token = MagicMock()
        self._get_expiration_date = MagicMock()
        self._set_mount_adapters = MagicMock()
        super().__init__(
            id, pasw, _Environment("http://catalogue.local"), "Test",
            logger=MagicMock(),
        )


class UnitTestClientMock(DliClient):

    def __init__(self, api_root, host=None, debug=None, strict=True,
                 access_id=None, secret_key=None, use_keyring=True):
        super().__init__("Test", access_id=access_id, secret_key=secret_key, use_keyring=use_keyring)

    def _new_session(self):
        return UnitTestSessionMock("Test", "Test")


class UnitTestSessionMockWithAuth(Session):

    def __init__(self, id, pasw):
        self.logger = MagicMock()
        self._set_mount_adapters = MagicMock()
        self.access_id = id
        self.secret_key = pasw
        self.auth_key = None
        self._environment = _Environment("http://catalogue.local")
        self.host = None
        self.use_keyring = True
        self.siren_builder = PatchedSirenBuilder()


class UnitTestClientMockWithAuth(UnitTestClientMock):

    def _new_session(self):
        return UnitTestSessionMockWithAuth(self.access_id, self.secret_key)


class UnitTestSessionMockNoPrompt(Session):

    # required to prevent the web popup that we want to
    # launch ourselves / use selenium
    def __init__(self, id, pasw, env):
        super().__init__(id, pasw, env, "Test",
                         auth_prompt=False, logger=MagicMock())


class UnitTestClientMockNoPrompt(DliClient):

    def _new_session(self):
        return UnitTestSessionMockNoPrompt(None, None, self._environment)


@pytest.fixture
def clear_keyring(monkeypatch):
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: None)
    monkeypatch.setattr(keyring, 'set_password', lambda _, app, val: None)

@pytest.fixture
def mock_session(clear_keyring):
    yield UnitTestSessionMock

@pytest.fixture
def mock_del_env_user(monkeypatch):
    monkeypatch.delenv("DLI_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("DLI_SECRET_ACCESS_KEY", raising=False)

@pytest.fixture
def real_client(request):
    # This is the S3 address used for the QA environment.
    api_root = os.environ[f'{request.param[0]}_API_URL']
    accessid = os.environ[f'{request.param[0]}_ACCESS_ID']
    secretkey = os.environ[f'{request.param[0]}_SECRET_ACCESS_KEY']
    client = None

    if request.param[1] == "Credentials":
        client = DliClient(
            api_root=api_root,
            access_id=accessid,
            secret_key=secretkey
        )
    elif request.param == 'API':
        pass
    else:
        pass

    yield client


@pytest.fixture
def mock_create_env_user(monkeypatch):
    monkeypatch.setenv("DLI_ACCESS_KEY_ID", "TestingUser")
    monkeypatch.setenv("DLI_SECRET_ACCESS_KEY", "TestingPass")


def test_credentials_no_api_key(monkeypatch, mock_create_env_user, recwarn):
    # test flow when u/p set and no api key set
    monkeypatch.setattr(DliClient, '_new_session', lambda x: x)
    dl = _start_session()
    assert(issubclass(type(dl), DliClient))
    assert(dl.secret_key is not None and dl.access_id is not None)


def test_credentials_session(mock_create_env_user, mock_session):
    # test flow when u/p set and no api key set

    sesh = mock_session(os.environ["DLI_ACCESS_KEY_ID"],
                        os.environ["DLI_SECRET_ACCESS_KEY"])
    assert sesh._get_SAM_auth_key.call_count == 1


def test_api_key_deprecation_warning(recwarn, monkeypatch):
    # test flow when u/p set and api key set
    # api key should override
    monkeypatch.setattr(DliClient, '_new_session', MagicMock())
    dl = _start_session(api_key="Test")
    assert(issubclass(type(dl), DliClient))
    assert "`api_key` will be deprecated in the future" \
           in ",".join([str(x.message) for x in recwarn.list])
    assert(dl.secret_key is not None and dl.access_id is None)


def test_credentials_and_api_key(
    clear_keyring, mock_create_env_user, monkeypatch
):
    # test flow when u/p set and api key set
    # api key should override
    monkeypatch.setattr(DliClient, '_new_session',  MagicMock())
    dl = _start_session(api_key="Test")
    assert (dl.secret_key is not None and dl.access_id is None)


def test_api_session(mock_create_env_user, mock_session):
    # test flow when u/p set and no api key set
    # (there will be no acces id set)
    sesh = mock_session(None, "Test")
    assert sesh._get_auth_key.call_count == 1


def test_credentials_and_no_api_key(
        clear_keyring, mock_create_env_user, monkeypatch, caplog
):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: UnitTestClientMock)
    dl = _start_session()
    for x in caplog.records:
        assert("old" not in x.message)


def test_no_credentials_and_api_key(mock_del_env_user, monkeypatch, caplog):
    # test flow when no credentials and api key set
    monkeypatch.setattr(session, "get_client", lambda: UnitTestClientMock)
    dl = _start_session(api_key="Test")
    assert (dl.secret_key is not None and dl.access_id is None)
    for x in caplog.records:
        assert("new" not in x.message)


def test_api_key_auth(mock_del_env_user, monkeypatch):
    # test old auth process (_get_auth_key())
    api_response = valid_token
    monkeypatch.setattr(session, "get_client", lambda: UnitTestClientMockWithAuth)
    dl = _start_session(api_key="API")
    dl._session.post = MagicMock()
    dl._session.post.return_value.text = api_response

    dl._session._auth_init()
    assert(dl and dl._session.auth_key is not None)


def test_credentials_auth(clear_keyring, mock_create_env_user, monkeypatch):
    # test new auth process (_get_SAM_auth_key())
    sam_response = {
        "access_token": valid_token,
        "token_type": "Bearer", "expires_in": 3599}
    catalogue_response = {
        "access_token": valid_token,
        "token_type": "Bearer", "expires_in": 3599}

    monkeypatch.setattr(session, "get_client", lambda: UnitTestClientMockWithAuth)
    dl = _start_session()
    dl._session.post = MagicMock()
    dl._session.post.return_value.json.side_effect = [
        sam_response, catalogue_response
    ]

    dl._session._auth_init()
    assert(dl and dl._session.auth_key is not None)



def real_drive(port, postbox, env):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    user = "dl_manual_test_2@ihsmarkit.com"
    pw = "-0o_p}i-Uz%*PQy_"

    driver = webdriver.Chrome(executable_path='tests/chromedriver',
                              options=chrome_options)

    driver.get(
        f"{env.catalogue}"
        f"{identity_urls.identity_postbox}"
        f"?postbox={postbox}"
    )

    WebDriverWait(driver, 120).until(
        ec.visibility_of_element_located((By.ID, "emailAddress"))
    ).send_keys(user)

    driver.find_element(By.ID, "continueButton").click()

    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.ID, "i0116"))
    ).send_keys(user)

    driver.find_element(By.ID, "idSIButton9").click()
    WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.NAME, "passwd"))
    ).send_keys(pw)

    driver.find_element(By.ID, "idSIButton9").click()

    driver.find_element(By.ID, "idSIButton9").click()
    # need to add some time, else the client quits before we
    # complete localhost activity.
    time.sleep(2)
    driver.quit()


def test_reload_JWT_keyring(monkeypatch):
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: valid_token)

    dl = UnitTestClientMockWithAuth(api_root="Test")
    dl._session._get_web_auth_key = MagicMock()
    dl._session._auth_init()
    assert dl._session._get_web_auth_key.call_count == 0


def test_reload_long_JWT_keyring(monkeypatch):
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: long_token)

    dl = UnitTestClientMockWithAuth(api_root="Test")
    dl._session._get_web_auth_key = MagicMock()
    dl._session._auth_init()
    assert dl._session.auth_key == long_token
    assert dl._session._get_web_auth_key.call_count == 0


@patch("os.name","nt")
def test_store_long_long_keyring_for_windows(monkeypatch, caplog):

    def errorout(domain, app, pasw):
        raise OSError("Key is too long")

    monkeypatch.setattr(keyring, 'set_password', errorout)
    dl = UnitTestClientMockWithAuth(api_root="Test")

    def catch(port, postbox):
        dl._session.get = MagicMock()
        dl._session.get.return_value = Mock(status_code=200, text="test", content="test")

    dl._session._get_web_auth_key(callback=catch)
    # n.b we are gonna get this, but because we play with os.name
    # we will vomit another exception about trying to use a window cred mgr
    assert 'Key is too long' in caplog.text

@patch("os.name","nt")
def test_store_long_long_keyring(monkeypatch, caplog):

    class TestKeyring(keyring.backend.KeyringBackend):
        priority = 1
        dic = {}

        def set_password(self, servicename, username, password):
            TestKeyring.dic[servicename+username] = password

        def get_password(self, servicename, username):
            return TestKeyring.dic[servicename+username]

        def delete_password(self, servicename, username, password):
            del TestKeyring.dic[servicename+username]

    tk = TestKeyring()
    old_keyring = keyring.get_keyring()
    keyring.set_keyring(tk)
    old = keyring.set_password

    def error_then_do(domain, app, pasw):
        keyring.set_password = old
        # impersonate the first Windows error
        raise OSError("Key is too long")

    keyring.set_password = error_then_do

    dl = UnitTestClientMockWithAuth(api_root="Test")

    def catch(port, postbox):
        dl._session.get = MagicMock()
        dl._session.get.return_value = Mock(status_code=200, text=valid_token, content="test")

    dl._session._get_web_auth_key(callback=catch)
    # n.b we are gonna get this, but because we play with os.name
    # we will vomit another exception about trying to use a window cred mgr
    keyring.set_keyring(old_keyring)
    assert len(tk.dic.keys()) == 2

    assert tk.dic["ihsm-datalakehttp://catalogue.local"] == "**split**1"
    assert tk.dic["ihsm-datalakehttp://catalogue.local-0"] == valid_token


@patch("os.name","nt")
def test_store_long_long_keyring_split(monkeypatch, caplog):

    class TestKeyring(keyring.backend.KeyringBackend):
        priority = 1
        dic = {}

        def set_password(self, servicename, username, password):
            TestKeyring.dic[servicename+username] = password

        def get_password(self, servicename, username):
            return TestKeyring.dic[servicename+username]

        def delete_password(self, servicename, username, password):
            del TestKeyring.dic[servicename+username]

    tk = TestKeyring()
    old_keyring = keyring.get_keyring()
    keyring.set_keyring(tk)
    old = keyring.set_password

    def error_then_do(domain, app, pasw):
        keyring.set_password = old
        raise OSError("Key is too long")


    keyring.set_password = error_then_do

    dl = UnitTestClientMockWithAuth(api_root="Test")

    def catch(port, postbox):
        dl._session.get = MagicMock()
        dl._session.get.return_value = Mock(status_code=200, text=long_token, content="test")

    dl._session._get_web_auth_key(callback=catch)
    # n.b we are gonna get this, but because we play with os.name
    # we will vomit another exception about trying to use a window cred mgr
    keyring.set_keyring(old_keyring)
    assert len(tk.dic.keys()) == 11

    assert tk.dic["ihsm-datalakehttp://catalogue.local"] == "**split**10"
    for x in range(int(tk.dic["ihsm-datalakehttp://catalogue.local"].split("**split**")[-1])):
        assert tk.dic[f"ihsm-datalakehttp://catalogue.local-{x}"] == \
               long_token[x*1000:((1+x)*1000)]

def test_no_reload_delete_expired_JWT_keyring(monkeypatch):

    dl = UnitTestClientMockWithAuth(api_root="Test")
    # we definitely set it in the first place
    keyring.set_password(
        __product__, dl._session._environment.catalogue, valid_token)
    # later 'expires'
    orig = keyring.get_password
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: expired_token)

    dl._session._get_web_auth_key = MagicMock()
    dl._session._get_web_auth_key.return_value = valid_token
    dl._session._auth_init()
    assert dl._session._get_web_auth_key.call_count == 1
    assert(orig(__product__, dl._session._environment.catalogue) is None)


@pytest.mark.skipif(os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
def test_set_JWT_keyring_web_auth_key(monkeypatch):
    orig = keyring.get_password
    monkeypatch.setattr(keyring, 'get_password', lambda _, app: None)
    dl = UnitTestClientMockWithAuth(api_root="Test")

    def catch(port, postbox):
        dl._session.get = MagicMock()
        dl._session.get.return_value = Mock(status_code=200, text=valid_token, content="test")

    dl._session._get_web_auth_key(callback=catch)
    assert(orig(__product__, dl._session._environment.catalogue)
           == valid_token)


@pytest.mark.xfail
@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
def test_web_flow(clear_keyring, mock_del_env_user, monkeypatch):

    monkeypatch.setattr(session, "get_client", lambda: UnitTestClientMockNoPrompt)
    dl = _start_session(root_url="https://catalogue-dev.udpmarkit.net")

    # this is what get_web_auth_key is otherwise doing,
    # but we need to unblock to allow selenium to operate.
    # so we register a custom default callback to call selenium
    # rather than the web browser
    def cb(port, postbox):
        real_drive(port, postbox, dl._environment)

    with patch.object(Session._get_web_auth_key, '__defaults__', (cb,)):
        dl._session._auth_init()

    assert dl._session.auth_key is not None

@pytest.mark.xfail
@pytest.mark.skipif(os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
@pytest.mark.parametrize('real_client', [('QA', "Credentials")],
                         indirect=['real_client'])
def test_credentials_on_catalogue(clear_keyring, real_client):
    # test that new auth actually works and returns JWT

    assert(real_client.datasets.get(
        "autotestdatasetItsdeclarationRomanZimmermannandpeople"
    ) is not None)

@pytest.mark.xfail
@pytest.mark.skipif(True or os.environ.get('CI_PYPI_USER') is not None,
                    reason="Not runnable on gitlab - 8080 closed")
@pytest.mark.integration
@pytest.mark.parametrize('real_client', [('QA', "Credentials")],
                         indirect=['real_client'])
def test_webflow_on_catalogue(monkeypatch, real_client):

    monkeypatch.setattr(session, "get_client", lambda: UnitTestClientMockNoPrompt)
    dl = _start_session(root_url="https://catalogue-dev.udpmarkit.net")

    # this is what get_web_auth_key is otherwise doing,
    # but we need to unblock to allow selenium to operate.
    # so we register a custom default callback to call selenium
    # rather than the web browser
    def cb(port, postbox):
        real_drive(port, postbox, dl._environment)

    with patch.object(Session._get_web_auth_key, '__defaults__', (cb,)):
        dl._session._auth_init()

    # todo - doesnt work with these u/p sam logins
    assert dl.datasets.get("Sheep") is not None


def test_no_system_keyring_installed(monkeypatch):
    keyring.core.set_keyring(keyring.core.fail.Keyring())
    monkeypatch.setattr("dli.client.dli_client.Session._reload_or_web_flow.__defaults__", (True,))
    try:
        from keyring.errors import NoKeyringError
        with pytest.raises(NoKeyringError):
            dl = _start_session(root_url="https://catalogue-dev.udpmarkit.net")
    except ImportError:
        with pytest.raises(RuntimeError):
            dl = _start_session(root_url="https://catalogue-dev.udpmarkit.net")


def test_no_system_keyring_ack(monkeypatch, capsys):
    keyring.core.set_keyring(keyring.core.fail.Keyring())
    a = Mock(status_code=200, text=valid_token, content="test")

    def t(pb):
        return a


    monkeypatch.setattr("dli.client.dli_client.Session._get_web_auth_key.__defaults__",
                        ( (lambda port, pb: t(pb)), ))
    monkeypatch.setattr(
        "dli.client.dli_client.Session.get",  (lambda port, pb: a)
    )

    dl = _start_session(root_url="https://catalogue-dev.udpmarkit.net")


    captured = capsys.readouterr()
    assert "no keyring manager available" in captured.out