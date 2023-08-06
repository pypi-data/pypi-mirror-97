"""Reusable test fixtures."""
import os
import pytest

from waylay import ClientCredentials, WaylayClient
from waylay.auth import WaylayTokenAuth

from waylay.service import ApiService, StorageService


def get_test_env(key: str, default: str = None) -> str:
    """Get an environment variable."""
    test_var = os.getenv(key, default)
    if not test_var:
        raise AttributeError(f'{key} environment variable not configured, while test requires it.')
    return test_var


@pytest.fixture
def waylay_test_profile():
    """Get environment variable WAYLAY_TEST_PROFILE."""
    return get_test_env('WAYLAY_TEST_PROFILE')


@pytest.fixture
def waylay_test_user_id():
    """Get environment variable WAYLAY_TEST_USER_ID."""
    return get_test_env('WAYLAY_TEST_USER_ID')


@pytest.fixture
def waylay_test_user_secret():
    """Get environment variable WAYLAY_TEST_USER_SECRET."""
    return get_test_env('WAYLAY_TEST_USER_SECRET')


@pytest.fixture
def waylay_test_accounts_url():
    """Get environment variable WAYLAY_TEST_ACCOUNTS_URL or 'https://accounts-api-staging.waylay.io'."""
    return get_test_env('WAYLAY_TEST_ACCOUNTS_URL', 'https://accounts-api-staging.waylay.io')


@pytest.fixture
def waylay_test_client_credentials(waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url):
    """Get client credentials.

    As specified in the environment variables
    WAYLAY_TEST_USER_ID, WAYLAY_TEST_USER_SECRET, WAYLAY_TEST_ACCOUNTS_URL
    """
    return ClientCredentials(
        waylay_test_user_id, waylay_test_user_secret, waylay_test_accounts_url
    )


@pytest.fixture
def waylay_test_token_string(waylay_test_client_credentials):
    """Get a valid token string."""
    token = WaylayTokenAuth(waylay_test_client_credentials).assure_valid_token()
    return token.token_string


@pytest.fixture
def waylay_test_client(waylay_test_client_credentials):
    """Get a test waylay SDK client."""
    waylay_client = WaylayClient.from_credentials(waylay_test_client_credentials)
    return waylay_client


@pytest.fixture
def waylay_storage(waylay_test_client: WaylayClient) -> StorageService:
    """Get the storage service."""
    return waylay_test_client.storage  # type: ignore


@pytest.fixture
def waylay_api(waylay_test_client: WaylayClient) -> ApiService:
    """Get the storage service."""
    return waylay_test_client.api  # type: ignore
