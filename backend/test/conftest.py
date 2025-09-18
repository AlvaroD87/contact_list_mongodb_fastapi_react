import pytest
import os

from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

os.environ["ENV_STATE"] = "test"

from backend.main import app
from backend.database import connect_to_mongo, close_mongo_connection


@pytest.fixture(scope="session") # runs ones for every session of testing
def anyio_backend():
    return "asyncio"

@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    # async with AsyncClient(app=app, base_url=client.base_url) as ac:
    async with AsyncClient(transport=ASGITransport(app=app), base_url=client.base_url) as ac:
        yield ac
