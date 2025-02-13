from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis.asyncio import ConnectionPool, Redis

from src.core.Base.singleton import Singleton
from src.core.settings import Configuration


class RedisSessionDependency(Singleton):
    def __init__(self) -> None:
        self._url = Configuration.settings.REDIS_URL
        self._pool: ConnectionPool = self._init_pool()

    def _init_pool(self) -> ConnectionPool:
        return ConnectionPool.from_url(self._url, encoding="utf-8", decode_responses=True, max_connections=20)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator:
        redis_client = Redis(connection_pool=self._pool)
        try:
            yield redis_client
        finally:
            await redis_client.aclose()
