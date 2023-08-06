"""Client configuration."""

from typing import (
    Optional, Mapping, MutableMapping, Any, Type
)
import os
import re
from pathlib import Path
import json
import logging
import httpx
from appdirs import user_config_dir
from .auth import (
    WaylayCredentials,
    NoCredentials,
    WaylayTokenAuth, WaylayToken,
    CredentialsCallback,
    parse_credentials,
    DEFAULT_ACCOUNTS_URL
)
from .auth_interactive import (
    request_client_credentials_interactive,
    request_store_config_interactive,
    _root_url_for
)
from .exceptions import AuthError, ConfigError

log = logging.getLogger(__name__)

# http client dependencies
_http = httpx

TenantSettings = Mapping[str, str]
Settings = MutableMapping[str, str]

DEFAULT_PROFILE = '_default_'
SERVICE_KEY_API = 'waylay_api'


class WaylayConfig():
    """Manages the authentication and endpoint configuration for the Waylay Platform."""

    profile: str
    _auth: WaylayTokenAuth
    _local_settings: Settings
    _tenant_settings: Optional[TenantSettings] = None

    _token_auth_provider: Type[WaylayTokenAuth] = WaylayTokenAuth

    DOC_URL: str = 'https://docs.waylay.io'
    IODOC_URL: str = 'https://docs-io.waylay.io/#'

    def __init__(
        self, credentials: WaylayCredentials = None, profile: str = DEFAULT_PROFILE,
        settings: TenantSettings = None, fetch_tenant_settings=True,
        credentials_callback: Optional[CredentialsCallback] = None
    ):
        """Create a WaylayConfig."""
        self.profile = profile
        if credentials is None:
            credentials = NoCredentials()
        self._local_settings = {}
        if settings:
            self.set_local_settings(**settings)
        self._auth = self._token_auth_provider(
            credentials, credentials_callback=credentials_callback
        )
        if not fetch_tenant_settings:
            self._tenant_settings = {}

    @property
    def credentials(self):
        """Get current credentials.

        As configured or returned by last callback).
        """
        return self._auth.credentials

    def get_root_url(
        self, config_key: str, default_root_url: Optional[str] = None, resolve_settings=True
    ) -> Optional[str]:
        """Get the root url for a waylay service."""
        config_key = _root_url_key_for(config_key)
        settings = self.get_settings(resolve=resolve_settings)
        url = settings.get(config_key, default_root_url)
        if url is not None:
            return _root_url_for(url)
        if default_root_url is None and config_key == SERVICE_KEY_API:
            domain = self.get_valid_token().domain
            if domain:
                return _root_url_for(domain)
        return None

    def set_root_url(self, config_key: str, root_url: Optional[str]):
        """Override the root url for the given server.

        Will persist on `save`.
        Setting a `None` value will remove the override.
        """
        config_key = _root_url_key_for(config_key)
        self.set_local_settings(**{config_key: root_url})

    @property
    def accounts_url(self):
        """Get the accounts url."""
        return _root_url_for(self.credentials.accounts_url)

    @property
    def tenant_settings(self) -> TenantSettings:
        """Get the tenant settings as stored on accounts.

        Will fetch settings when not present and initialised with 'fetch_tenant_settings=True'.
        """
        if self._tenant_settings is None:
            self._tenant_settings = self._request_settings()

        return self._tenant_settings

    @property
    def local_settings(self) -> TenantSettings:
        """Get the settings overrides for this configuration.

        These include the endpoint overrides that are stored with the profile.
        """
        return self._local_settings

    def set_local_settings(self, **settings: Optional[str]) -> TenantSettings:
        """Set a local endpoint url override for a service."""
        for config_key, value in settings.items():
            if value is None and config_key in self._local_settings:
                del self._local_settings[config_key]
            if value is not None:
                self._local_settings[config_key] = value
        return self.local_settings

    @property
    def settings(self) -> TenantSettings:
        """Get settings, from tenant configuration and local overrides."""
        return self.get_settings(resolve=True)

    def get_settings(self, resolve=True) -> TenantSettings:
        """Get the tenant settings.

        As resolved form the accounts backend, and overridden with local settings.
        If `resolve=True`, fetch and cache tenant settings from the accounts backend.
        """
        return {
            **(self.tenant_settings if resolve else self._tenant_settings or {}),
            **self.local_settings
        }

    def get_valid_token(self) -> WaylayToken:
        """Get the current valid authentication token or fail."""
        if isinstance(self.auth, WaylayTokenAuth):
            try:
                return self.auth.assure_valid_token()
            except AuthError as exc:
                raise ConfigError(f'Cannot get valid token: {exc}') from exc
        raise ConfigError('not using token authentication')  # pragma: no cover

    @property
    def auth(self) -> _http.Auth:
        """Get the current the http authentication interceptor."""
        return self._auth

    @property
    def domain(self) -> Optional[str]:
        """Get the Waylay domain of the current user."""
        try:
            return self.get_valid_token().domain
        except ConfigError:
            return None

    def _request_settings(self) -> TenantSettings:
        try:
            settings_url = f"{self.get_root_url('api', resolve_settings=False)}/api/settings"
            settings_resp = _http.get(settings_url, auth=self.auth)
            settings_resp.raise_for_status()
            return {
                key: value
                for key, value in settings_resp.json().items()
                if key.startswith('waylay_')
            }
        except _http.HTTPStatusError as exc:
            if exc.response.status_code == 403:
                log.warning(
                    "You are not authorised to fetch tenant settings.\n"
                    "The Waylay SAAS defaults will be used, unless you\n"
                    "provide explicit overrides in the SDK Configuration profile."
                )
                return {}
            raise ConfigError('cannot resolve tenant settings') from exc  # pragma: no cover
        except _http.HTTPError as exc:
            raise ConfigError('cannot resolve tenant settings') from exc  # pragma: no cover

    # config persistency methods
    @classmethod
    def config_file_path(cls, profile: str = DEFAULT_PROFILE) -> str:
        """Compute the default OS path used to store this configuration."""
        return os.path.join(user_config_dir('Waylay'), 'python_sdk', f".profile.{profile}.json")

    @classmethod
    def load(
        cls,
        profile: str = DEFAULT_PROFILE,
        interactive: bool = True,
        accounts_url: str = DEFAULT_ACCOUNTS_URL
    ):
        """Load a stored waylay configuration."""
        try:
            with open(cls.config_file_path(profile), mode='r') as config_file:
                config_json = json.load(config_file)
            return cls.from_dict(config_json)
        except FileNotFoundError as exc:
            if not interactive:
                raise ConfigError(f'Config profile {profile} not found') from exc
            credentials = request_client_credentials_interactive(accounts_url)
            instance = cls(
                credentials,
                profile=profile
            )
            request_store_config_interactive(profile, save_callback=instance.save)
            return instance

    @classmethod
    def from_dict(cls, config_json: Mapping[str, Any]):
        """Create a WaylayConfig from a dict representation."""
        config_json = dict(config_json)
        if 'credentials' in config_json:
            config_json['credentials'] = parse_credentials(config_json['credentials'])
        return cls(**config_json)

    def to_dict(self, obfuscate=True):
        """Get the (obfuscated) attributes of this WaylayConfig.

        Secret credentials are obfuscated.
        """
        return {
            'credentials': self.credentials.to_dict(obfuscate),
            'profile': self.profile,
            'settings': self.local_settings
        }

    def save(self) -> str:
        """Save the configuration as specified in the profile.

        Returns the save location.
        """
        config_path = Path(self.config_file_path(self.profile))
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, mode='w') as config_file:
            json.dump(self.to_dict(obfuscate=False), config_file)
            log.info("wrote waylay configuration: %s", config_path)
        return str(config_path)

    @classmethod
    def delete(cls, profile: str = DEFAULT_PROFILE) -> str:
        """Delete a stored profile.

        Returns the deleted location.
        """
        config_path = Path(cls.config_file_path(profile))
        if config_path.exists():
            config_path.unlink()
            log.warning("waylay configuration removed: %s", config_path)
        else:
            log.warning("waylay configuration not found: %s", config_path)
        return str(config_path)

    @classmethod
    def list_profiles(cls):
        """List stored config profiles."""
        config_dir = Path(cls.config_file_path()).parent
        return {
            re.match(r'\.profile\.(.*)\.json', config_file.name)[1]: str(config_file)
            for config_file in config_dir.iterdir()
        }

    def __repr__(self):
        """Show the implementation class an main attributes."""
        return f'<WaylayConfig({str(self)})>'

    def __str__(self):
        """Show the main (obfuscated) attributes as a string."""
        return json.dumps(self.to_dict(obfuscate=True))


def _root_url_key_for(config_key: str):
    if config_key.startswith('waylay_'):
        return config_key
    return f"waylay_{config_key}"
