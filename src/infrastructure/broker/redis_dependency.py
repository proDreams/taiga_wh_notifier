from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from redis.asyncio import ConnectionPool, Redis

from src.core.Base.singleton import Singleton
from src.core.settings import get_settings


class RedisSessionDependency(Singleton):
    """
    Manages a singleton instance of a Redis session dependency.

    Provides an asynchronous context manager for managing connections to a Redis database.
    """

    def __init__(self) -> None:
        """
        Initializes the Redis connection pool for caching operations.

        :ivar self._url: The URL of the Redis server configured in the application settings.
        :type self._url: str
        :ivar self._pool: The connection pool used to manage connections to the Redis server.
        :type self._pool: ConnectionPool
        """
        self._url = get_settings().REDIS_URL
        self._pool: ConnectionPool = self._init_pool()

    def _init_pool(self) -> ConnectionPool:
        """
        Initializes a connection pool for database connections.

        :returns: A ConnectionPool object configured with the specified URL and settings.
        :rtype: ConnectionPool
        """
        return ConnectionPool.from_url(
            self._url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=get_settings().REDIS_MAX_CONNECTIONS,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator:
        """
        Provides asynchronous session management for Redis client.

        This method creates and manages a context manager for an AsyncGenerator that yields a Redis client.
        The session ensures the Redis connection is properly closed after use.

        :return: An AsyncGenerator that yields an instance of Redis client.
        :rtype: AsyncGenerator
        """
        redis_client = Redis(connection_pool=self._pool)
        try:
            yield redis_client
        finally:
            await redis_client.aclose()
