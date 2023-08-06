"""Bridge: Client"""
import async_timeout

from asyncio import get_event_loop
from aiohttp import ClientSession, ClientResponse

from ..objects.base import BridgeBase
from ..exceptions import BridgeException, BridgeAuthenticationException


class BridgeClient(BridgeBase):
    """Client to handle API calls."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize the client."""
        self._session = session

    async def get(self, url: str, **kwargs) -> ClientResponse:
        """Make a GET request."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> ClientResponse:
        """Make a POST request."""
        return await self.request("POST", url, **kwargs)

    async def request(
        self, method: str in ["GET", "POST"], url: str, **kwargs
    ) -> ClientResponse:
        """Make a request."""
        async with async_timeout.timeout(20, loop=get_event_loop()):
            response: ClientResponse = await self._session.request(
                method,
                url,
                **kwargs,
            )
        if response.status not in (200, 201, 202, 204):
            if response.status == 401:
                raise BridgeAuthenticationException(
                    {
                        "request": {
                            "method": method,
                            "url": url,
                            **kwargs,
                        },
                        "response": await response.json(),
                        "status": response.status,
                    }
                )
            else:
                raise BridgeException(
                    {
                        "request": {
                            "method": method,
                            "url": url,
                            **kwargs,
                        },
                        "response": await response.json(),
                        "status": response.status,
                    }
                )
        return response
