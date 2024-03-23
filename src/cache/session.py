from redis import asyncio as aioredis
from redis.asyncio import Redis
from src.config import app_config


pool = aioredis.ConnectionPool.from_url(app_config.REDIS_URL, max_connections=10)


async def get_redis_session() -> Redis:
    async with aioredis.Redis(connection_pool=pool) as session:
        yield session
