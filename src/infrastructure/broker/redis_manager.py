from fastapi import Depends

from src.infrastructure.broker.redis_dependency import RedisSessionDependency


class RedisManager:
    """
    Manages interactions with a Redis database using an asynchronous session dependency.
    """

    def __init__(self, redis_dep: RedisSessionDependency = Depends(RedisSessionDependency)) -> None:
        """
        Initializes the instance of the class with a Redis session dependency.

        :param redis_dep: Dependency injection for Redis session management.
        :type redis_dep: RedisSessionDependency
        """
        self._redis_dep = redis_dep

    async def set_data(self, key: str, value: str) -> None:
        """
        Sets data in the Redis database asynchronously.

        :param key: The key under which the value will be stored.
        :type key: str
        :param value: The value to be set for the given key.
        :type value: str
        """
        async with self._redis_dep.session() as session:
            await session.set(key, value)

    async def delete_data(self, key: str) -> None:
        """
        Deletes a key from the Redis database.

        :param key: The key to be deleted.
        :type key: str
        """
        async with self._redis_dep.session() as session:
            await session.delete(key)
