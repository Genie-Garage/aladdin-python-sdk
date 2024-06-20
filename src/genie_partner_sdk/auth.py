from abc import abstractmethod
from aiohttp import ClientSession, ClientResponse
import logging


class Auth:
    """Class to make authenticated requests"""

    def __init__(self, websession: ClientSession, host: str, access_token: str, api_key: str):
        """Initialize the auth."""
        self._logger = logging.getLogger(__name__)
        self.websession = websession
        self.host = host
        self.access_token = access_token
        self.api_key = api_key

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"
        headers["x-api-key"] = self.api_key

        return await self.websession.request(
            method, f"{self.host}/{path}", **kwargs, headers=headers,
        )
