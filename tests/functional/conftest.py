import asyncio
from dataclasses import dataclass

import aiohttp
import pytest
import pytest_asyncio

from settings import settings

pytest_plugins = []


@pytest_asyncio.fixture(scope="session")
async def client_session(event_loop):
    session = aiohttp.ClientSession(loop=event_loop)
    yield session
    await session.close()


@pytest.fixture(scope="session")
def web_client(client_session):
    return Client(
        host=settings.api_host,
        port=settings.api_port,
        session=client_session,
    )


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@dataclass
class Client:
    host: str
    port: int
    session: aiohttp.ClientSession

    async def get(self, uri: str, **kwargs) -> aiohttp.ClientResponse:
        response = await self.session.get(
            f"http://{self.host}:{self.port}/api/v1" + uri, **kwargs
        )
        return response
