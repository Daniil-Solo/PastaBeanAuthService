import asyncio
from fastapi import status
from typing import AsyncGenerator
from redis import asyncio as aioredis
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from integration_tests.urls import REGISTER_URL
from src.dto.user import UserRegisterDTO
from integration_tests.constants import USER_NAME, USER_PASSWORD, USER_EMAIL
from src.app import create_application
from src.config import app_config
from src.database.session import get_async_session, async_engine
from src.cache.session import get_redis_session
from src.database.models import Base

engine_test = create_async_engine(app_config.test_db_url, poolclass=NullPool)
test_async_session_factory = async_sessionmaker(
    bind=async_engine, autocommit=False, autoflush=False
)
Base.metadata.bind = engine_test


async def override_get_redis_session() -> aioredis.Redis:
    async with aioredis.Redis(host=app_config.TEST_CACHE_HOST, port=app_config.TEST_CACHE_PORT) as session:
        yield session


async def override_get_async_session() -> AsyncSession:
    async with test_async_session_factory() as session:
        yield session


@pytest.fixture(scope="session")
def test_app() -> FastAPI:
    app = create_application()
    app.dependency_overrides[get_async_session] = override_get_async_session
    app.dependency_overrides[get_redis_session] = override_get_redis_session
    return app


@pytest.fixture(scope="session")
async def async_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://localhost") as ac:
        yield ac


@pytest.fixture(scope='function', autouse=True)
async def prepare_storages():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    cache = aioredis.Redis(host=app_config.TEST_CACHE_HOST, port=app_config.TEST_CACHE_PORT)
    await cache.flushall()
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await cache.flushall()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def register_one_user(async_client: AsyncClient):
    valid_response = await async_client.post(
        url=REGISTER_URL,
        json=UserRegisterDTO(name=USER_NAME, email=USER_EMAIL, password=USER_PASSWORD).model_dump()
    )
    assert valid_response.status_code == status.HTTP_200_OK
