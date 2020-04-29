"""Package to interact with Worx Landroid Cloud API."""

import json
import logging
from os import path
from tempfile import gettempdir
from typing import Any, List, Optional

from oauthlib.oauth2 import LegacyApplicationClient, TokenExpiredError
from ratelimit import limits, sleep_and_retry
from requests import Response
from requests_oauthlib import OAuth2Session

from pylandroidcloud.models import Mower, MowerStatus

TOKEN_FILE = path.join(gettempdir(), "LANDROID_TOKEN_FILE")
API_LIMIT = 60

DEFAULT_TIMEOUT = 30

BASE_URL = "https://api.worxlandroid.com/api/v2"
WORX_TOKEN = BASE_URL + "/oauth/token"

_LOGGER = logging.getLogger(__name__)


class LandroidAPI:
    """Interact with Worx Landroid API Authentication."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        token_file: Optional[str] = TOKEN_FILE,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
    ):
        """Initialize the data object."""
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._timeout = timeout
        self._token_file = str(token_file)

        self._client = OAuth2Session(
            client=LegacyApplicationClient(client_id=client_id)
        )
        self.get_token()

    def fetch_token(self, authorization_response: Optional[str] = None) -> None:
        """Return authorization token for session."""
        token = self._client.fetch_token(
            WORX_TOKEN,
            authorization_response=authorization_response,
            username=self._username,
            password=self._password,
            client_id=self._client_id,
            client_secret=self._client_secret,
        )

        if token is not None:
            self._client.token = token
            self.write_token_file()

    def refresh_token(self) -> None:
        """Refresh and return new Worx Landroid API tokens."""
        token = self._client.refresh_token(WORX_TOKEN)

        if token is not None:
            self._client.token = token
            self.write_token_file()

    def write_token_file(self) -> None:
        """Write token locally."""
        with open(self._token_file, "w") as token_file:
            token_file.write(json.dumps(self._client.token))

    def read_token_file(self) -> None:
        """Read local token file and load it."""
        with open(self._token_file, "r") as token_file:
            self._client.token = json.load(token_file)

    def get_token(self) -> None:
        """Read local token file and load it."""
        try:
            if not self._client.token:
                self.read_token_file()
        except FileNotFoundError:
            _LOGGER.debug(f"Token file does not exist, fetching new token")
            self.fetch_token()

    def get_client(self) -> OAuth2Session:
        """Return the underlying client"""
        return self._client


class LandroidClient:
    """Generic API client"""

    def __init__(self, api: LandroidAPI, timeout: Optional[int] = DEFAULT_TIMEOUT):
        """Initialize the data object."""
        self._api = api
        self._timeout = timeout

    def get(self, url: str) -> Response:
        """Fetch a URL with GET method."""
        return self._request("get", url)

    def _request(self, method: str, url_path: str, **kwargs: Any) -> Response:
        url = BASE_URL + url_path
        try:
            return getattr(self._api.get_client(), method)(
                url, timeout=self._timeout, **kwargs
            )
        except TokenExpiredError:
            self._api.refresh_token()
            return getattr(self._api.get_client(), method)(
                url, timeout=self._timeout, **kwargs
            )


class LandroidMowerList(LandroidClient):
    """Get mower list from Worx Landroid API."""

    def __init__(self, api: LandroidAPI, timeout: Optional[int] = DEFAULT_TIMEOUT):
        """Initialize the data object."""
        super().__init__(api, timeout)
        self.mowers = self.get_mowers()

    def get_mowers(self) -> List[Mower]:
        """Return all available mowers from Worx Landroid API."""
        response = self.get("/product-items")
        response.raise_for_status()

        _LOGGER.debug(f"get_mowers Response: {response.text}")
        return [Mower(**s) for s in response.json()]


class LandroidMower(LandroidClient):
    """Get single mower data from Worx Landroid API."""

    def __init__(
        self,
        api: LandroidAPI,
        serial_number: str,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
    ):
        """Initialize the data object."""
        super().__init__(api, timeout)
        self._serial_number = serial_number
        self.mower = self.get_mower()

    def get_mower(self) -> Mower:
        """Return all available mowers from Worx Landroid API."""
        response = self.get("/product-items/{id}".format(id=self._serial_number))
        response.raise_for_status()

        _LOGGER.debug(f"get_mower Response: {response.text}")
        return Mower(**response.json())


class LandroidMowerState(LandroidClient):
    """Get the latest mower status data and update the states."""

    def __init__(
        self,
        api: LandroidAPI,
        serial_number: str,
        update_on_init: Optional[bool] = True,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
    ):
        """Initialize the data object."""
        super().__init__(api, timeout)
        self._serial_number = serial_number
        self.state = None
        if update_on_init:
            self.update()

    @sleep_and_retry
    @limits(calls=2, period=API_LIMIT)
    def update(self) -> None:
        """Return updated value for session."""
        return self.update_force()

    def update_force(self) -> None:
        """Return updated value for session without auto retry or limits."""
        response = self.get("/product-items/{id}/status".format(id=self._serial_number))
        response.raise_for_status()

        _LOGGER.debug(f"update_force Response: {response.text}")

        self.state = MowerStatus(**response.json())  # type: ignore
