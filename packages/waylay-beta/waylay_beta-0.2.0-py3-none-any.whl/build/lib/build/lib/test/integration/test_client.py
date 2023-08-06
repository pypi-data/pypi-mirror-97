"""Integration tests for waylay.auth module."""
from waylay import (
    WaylayClient
)

import waylay.config
import waylay.auth_interactive
from waylay.config import (
    DEFAULT_PROFILE
)


def test_create_client_from_credentials(
    waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url
):
    """Test authentication with client credentials."""
    waylay_client = WaylayClient.from_client_credentials(
        waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url
    )
    assert waylay_client.config is not None

    cfg = waylay_client.config
    assert cfg.profile == DEFAULT_PROFILE

    cred = cfg.credentials
    assert cred.api_key == waylay_test_user_id
    assert cred.api_secret == waylay_test_user_secret
    assert cred.accounts_url == waylay_test_accounts_url

    analytics_version = waylay_client.analytics.about.version()
    assert 'tsanalytics.server 0.' in analytics_version


def test_create_client_from_profile(
    waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url, monkeypatch
):
    """Test profile creation dialog."""
    user_dialog = (response for response in [
        "alternative endpoint", waylay_test_accounts_url,
        "apiKey", waylay_test_user_id,
        "apiSecret", waylay_test_user_secret,
        "store these credentials", 'N'
    ])

    def mock_ask(prompt: str, secret: bool = False) -> str:
        assert secret == ('Secret' in prompt)
        assert next(user_dialog) in prompt
        return next(user_dialog)

    monkeypatch.setattr(waylay.auth_interactive, 'ask', mock_ask)
    waylay_client = WaylayClient.from_profile('example', accounts_url=waylay_test_accounts_url)
    root_url = waylay_client.list_root_urls()
    assert 'analytics' in root_url
