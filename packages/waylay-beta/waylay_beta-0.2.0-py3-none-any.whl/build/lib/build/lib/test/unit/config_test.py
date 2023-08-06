"""Test suite for package `waylay.config`."""

import pytest
from datetime import datetime

from waylay import WaylayConfig, ClientCredentials
from waylay.exceptions import ConfigError
from waylay.auth import (
    WaylayTokenAuth, WaylayToken, AuthError,
    TokenCredentials, NoCredentials,
    DEFAULT_ACCOUNTS_URL
)
from httpx import Response, Request

MOCK_DOMAIN = 'unittest.waylay.io'
MOCK_API_URL = f'https://{MOCK_DOMAIN}'

MOCK_TOKEN_DATA = {
    'domain':  MOCK_DOMAIN,
    'tenant': '9999999999999999999999',
    'sub': 'users/999999999999999',
    'exp': datetime.now().timestamp() + 100000
}

MOCK_TENANT_SETTINGS = {
    'waylay_api': MOCK_API_URL,
    'waylay_domain': MOCK_DOMAIN
}


class WaylayTokenStub(WaylayToken):
    """A WaylayToken test stub with fixed data."""

    def __init__(self):
        """Create a WaylayTokenStub."""
        super().__init__('', MOCK_TOKEN_DATA)


def _mock_send_single_request_accounts(target, request: Request, *args) -> Response:
    return Response(status_code=200, request=request, json=MOCK_TENANT_SETTINGS)


def _mock_send_single_request_no_accounts(target, request: Request, *args) -> Response:
    return Response(status_code=403, request=request)


@pytest.fixture
def mock_token(mocker):
    """Mock the auth module to use a WaylayTokenStub."""
    mocker.patch('waylay.auth._request_token_from_accounts', lambda *args: '')
    mocker.patch('waylay.auth.WaylayTokenAuth._create_and_validate_token', lambda *args: WaylayTokenStub())


@pytest.fixture
def mock_httpx_accounts(mocker):
    """Mock the httpx module to return an accounts settings http response."""
    mocker.patch('httpx._client.Client._send_single_request', _mock_send_single_request_accounts)


@pytest.fixture
def mock_httpx_no_accounts(mocker):
    """Mock the httpx module to fail to authenticate an accounts settings http request."""
    mocker.patch('httpx._client.Client._send_single_request', _mock_send_single_request_no_accounts)


def test_empty_config():
    """Test an unconfigured WaylayConfig."""
    cfg = WaylayConfig()
    assert isinstance(cfg.auth, WaylayTokenAuth)
    assert cfg.local_settings == {}
    assert cfg.domain is None
    assert isinstance(cfg.credentials, NoCredentials)
    for property_callback in [
        lambda: cfg.tenant_settings,
        lambda: cfg.tenant_settings,
        lambda: cfg.get_root_url('a_service'),
        lambda: cfg.get_root_url('api'),
    ]:
        with pytest.raises(ConfigError) as exc:
            property_callback()
        assert 'Cannot get valid token: No credentials' in format(exc.value)


def test_config_settings():
    """Test handling of local settings."""
    cfg = WaylayConfig()
    local_settings = {'waylay_api': 'xxx', 'waylay_abc': 'http://yyy/'}
    cfg = WaylayConfig(settings=local_settings, fetch_tenant_settings=False)
    assert cfg.local_settings == local_settings
    assert cfg.tenant_settings == {}
    assert cfg.settings == local_settings
    assert cfg.domain is None
    assert cfg.accounts_url == DEFAULT_ACCOUNTS_URL
    assert isinstance(cfg.credentials, NoCredentials)
    assert cfg.get_root_url('a_service') is None
    assert cfg.get_root_url('api') == 'https://xxx'
    assert cfg.get_root_url('abc') == 'http://yyy'


def test_tenant_settings(mock_httpx_accounts, mock_token):
    """Test handling of tenant accounts settings."""
    local_settings = {'waylay_api': 'xxx', 'waylay_abc': 'http://yyy/'}
    cfg = WaylayConfig(credentials=TokenCredentials('_'), settings=local_settings)
    assert cfg.local_settings == local_settings
    assert cfg.tenant_settings == MOCK_TENANT_SETTINGS
    assert cfg.settings == {**MOCK_TENANT_SETTINGS, **local_settings}
    assert cfg.domain == MOCK_DOMAIN
    assert cfg.credentials.token == '_'
    assert cfg.get_root_url('a_service') is None
    assert cfg.get_root_url('api') == 'https://xxx'
    assert cfg.get_root_url('abc') == 'http://yyy'


def test_empty_config_no_accounts(mock_httpx_no_accounts, mock_token):
    """Test handling of failure to retrieve accounts settings."""
    cfg = WaylayConfig(credentials=TokenCredentials('_'))
    assert isinstance(cfg.auth, WaylayTokenAuth)
    assert cfg.local_settings == {}
    assert cfg.tenant_settings == {}
    assert cfg.settings == {}
    assert cfg.domain == MOCK_DOMAIN
    assert cfg.get_root_url('a_service') is None
    assert cfg.get_root_url('api') == MOCK_API_URL


def test_get_set_root_url(mock_httpx_accounts, mock_token):
    """Test setting of root urls for services."""
    cfg = WaylayConfig(credentials=TokenCredentials('_'))

    assert cfg.get_root_url('a_service') is None
    assert cfg.get_root_url('a_service', 'xxx.waylay.io') == 'https://xxx.waylay.io'
    cfg.set_root_url('a_service', 'http://a_service.waylay.io/api/')
    assert cfg.get_root_url('a_service') == 'http://a_service.waylay.io/api'
    cfg.set_local_settings(waylay_a_service='yyy.waylay.io')
    assert cfg.get_root_url('a_service') == 'https://yyy.waylay.io'
    assert cfg.get_root_url('waylay_a_service') == 'https://yyy.waylay.io'

    cfg.set_local_settings(waylay_a_service=None)
    assert cfg.get_root_url('a_service') is None

    assert cfg.get_root_url('api') == MOCK_API_URL


def test_representations(mock_httpx_accounts, mock_token):
    """Test the __str__ and __repr__ representations."""
    cfg = WaylayConfig(
        credentials=TokenCredentials('_'),
        settings=dict(a='b')
    )
    assert '"a": "b"' in str(cfg)
    assert '"token": "***' in str(cfg)
    assert '"a": "b"' in repr(cfg)
    assert '"token": "***' in repr(cfg)
    assert '***' in cfg.to_dict()['credentials']['token']
    assert '_' == cfg.to_dict(obfuscate=False)['credentials']['token']


def test_save_load_delete_profile(mock_httpx_accounts, mock_token):
    """Test saving, loading and deletion of config profiles."""
    profile_name = f'_unit_test_{int(datetime.now().timestamp())}'
    with pytest.raises(ConfigError) as exc:
        WaylayConfig.load(profile_name, interactive=False)
    assert 'not found' in format(exc.value)

    cfg = WaylayConfig(
        profile=profile_name,
        credentials=TokenCredentials('_'),
        settings=dict(a='b')
    )

    cfg.save()

    cfg_saved = WaylayConfig.load(profile_name)
    assert cfg_saved.settings == cfg.settings

    assert any(profile_name in profile for profile in WaylayConfig.list_profiles())

    WaylayConfig.delete(profile_name)
    WaylayConfig.delete(profile_name)

    with pytest.raises(ConfigError) as exc:
        WaylayConfig.load(profile_name, interactive=False)
    assert 'not found' in format(exc.value)


def test_load_interactive(mocker, mock_token):
    """Test the interactive handling of loading a config."""
    mocker.patch('waylay.config.request_client_credentials_interactive', lambda *args: TokenCredentials('_'))
    mocker.patch('waylay.config.request_store_config_interactive', lambda profile, save_callback: save_callback())

    profile_name = f'_unit_test_{int(datetime.now().timestamp())}'
    cfg = WaylayConfig.load(profile_name)

    assert cfg.credentials.token == '_'

    assert any(profile_name in profile for profile in WaylayConfig.list_profiles())

    WaylayConfig.delete(profile_name)

    assert not any(profile_name in profile for profile in WaylayConfig.list_profiles())
