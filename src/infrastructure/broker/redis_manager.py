import textwrap

from src.infrastructure.broker.redis_dependency import RedisSessionDependency


class RedisManager:
    """
    Manages interactions with a Redis database using an asynchronous session dependency.
    """

    def __init__(self) -> None:
        """
        Initializes the instance of the class with a Redis session dependency.

        :param redis_dep: Dependency injection for Redis session management.
        :type redis_dep: RedisSessionDependency
        """
        self._redis_dep = RedisSessionDependency()
        self._lock_time = 30  # sec

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

    async def is_exists(self, key: str) -> bool:
        async with self._redis_dep.session() as session:
            result = await session.exists(key)
        return result != 0

    async def add_wh_to_sorted_set(self, key: str, value: str, timestamp: int) -> None:
        # TOD Docstring
        async with self._redis_dep.session() as session:
            await session.zadd(key, {value: timestamp})

    async def get_wh_sorted_list(self, key: str) -> list | None:
        # TOD Docstring
        get_sorted_list_and_delete_queue_lua_script = textwrap.dedent(
            """
            local sorted_list = redis.call('ZRANGE', KEYS[1], 0, -1)
            redis.call('DEL', KEYS[1])
            return sorted_list
            """
        )
        async with self._redis_dep.session() as session:
            wh_sorted_list = await session.eval(get_sorted_list_and_delete_queue_lua_script, 1, key)
            return wh_sorted_list

    async def set_if_not_exist(self, key: str, value: str) -> None:
        # TOD
        """ """
        async with self._redis_dep.session() as session:
            # return await session.setnx(key, value)
            return await session.zadd(key, value)

    async def get_data(self, key: str) -> None:
        # TOD
        """ """
        async with self._redis_dep.session() as session:
            return await session.get(key)

    async def lock_data(self, lock_key: str, worker_id: str):
        async with self._redis_dep.session() as session:
            return await session.set(name=lock_key, value=worker_id, nx=True, ex=self._lock_time)

    async def is_locked_by_worker_id(self, lock_key: str, worker_id: str):
        async with self._redis_dep.session() as session:
            return await session.get(name=lock_key) == worker_id

    async def unlock_data(self, lock_key: str, worker_id: str):
        async with self._redis_dep.session() as session:
            if await session.get(name=lock_key) != worker_id:
                raise Exception("Something went wrong")
            session.delete(name=lock_key)
