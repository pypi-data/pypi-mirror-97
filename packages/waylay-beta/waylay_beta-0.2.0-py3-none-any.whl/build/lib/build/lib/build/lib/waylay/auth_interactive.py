"""Interactive authentication callback for client credentials."""

from typing import Optional
import logging
import re

import urllib.parse

from getpass import getpass
import httpx

from .auth import (
    WaylayCredentials,
    ClientCredentials,
    DEFAULT_ACCOUNTS_URL,
    AuthError
)

_http = httpx

log = logging.getLogger(__name__)


def tell(message: str):
    """Show an interactive authentication message."""
    print(message)


def ask(prompt: str, secret: bool = False) -> str:
    """Prompt user for credential information."""
    if secret:
        return getpass(prompt=prompt)
    return input(prompt)


def request_client_credentials_interactive(default_accounts_url: str = DEFAULT_ACCOUNTS_URL) -> WaylayCredentials:
    """Asks interactively for client credentials.

    Default callback provider for an interactive WaylayConfig.
    """
    tell("Authenticating to the Waylay Platform")

    accounts_url: str = default_accounts_url
    acc_validated = False
    while not acc_validated:
        tell(f'Using authentication provider at [{accounts_url}]')
        accounts_url = ask(
            '> alternative endpoint (press enter to continue)?: '
        ) or accounts_url
        accounts_url = _root_url_for(accounts_url)
        accounts_status_resp = httpx.get(accounts_url)
        acc_validated = not accounts_status_resp.is_error
        if acc_validated:
            tell(f"Authenticating at '{accounts_status_resp.json()['name']}'")
        else:
            tell(f"Cannot connect to '{accounts_url}': {accounts_status_resp.reason_phrase}")

    tell("Please provide client credentials for the waylay data client.")
    credentials = ClientCredentials(api_key='', api_secret='', accounts_url=accounts_url)
    retry = 0
    while not credentials.is_well_formed() and retry < 3:
        api_key = ask(prompt='> apiKey : ', secret=False).strip()
        api_secret = ask(prompt='> apiSecret : ', secret=True).strip()
        credentials = ClientCredentials(
            api_key=api_key, api_secret=api_secret, accounts_url=accounts_url
        )
        if not credentials.is_well_formed():
            retry += 1
            if retry >= 3:
                tell('Too many attempts, failing authentication')
                raise AuthError('Too many attempts, failing authentication')
            tell('Invalid apiKey or apiSecret, please retry')
    return credentials


def request_store_config_interactive(profile, save_callback):
    """Save interactively the storage of credentials as a profile."""
    store = ''
    while not store or store[0].lower() not in ('n', 'y', 't', 'f'):
        store = ask(
            f'> Do you want to store these credentials with profile={profile}? [Y]: '
        ) or 'Y'
    if store[0].lower() in ('y', 't'):
        save_location = save_callback()
        tell(
            f"Credential configuration stored as \n\t{save_location}\n"
            "Please make sure this file is treated securely.\n"
            "If compromised, _Revoke_ the api-key on the Waylay Console!"
        )


def _root_url_for(host_or_url: str) -> str:
    scheme, loc, path, query, fragment = urllib.parse.urlsplit(host_or_url)

    if not scheme and not loc:
        # make sure any host name is converted in a https:// url
        scheme = 'https'
        loc = path
        path = ''

    if path.endswith('/'):
        # tenant settings root urls are without trailing slash
        log.warning('Trailing slashes trimmed: %s', host_or_url)
        path = path.rstrip('/')

    return urllib.parse.urlunsplit([scheme, loc, path, query, fragment])
