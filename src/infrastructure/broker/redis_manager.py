import textwrap

from src.infrastructure.broker.redis_dependency import RedisSessionDependency


class RedisManager:
    """
    Manages interactions with a Redis database using an asynchronous session dependency.
    """

    def __init__(self, redis_dep: RedisSessionDependency) -> None:
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

    async def add_wh_to_sorted_set(self, key: str, value: str, timestamp: int) -> bool:
        """
        Adds a value to a Redis sorted set, and returns whether the sorted set already existed.

        This method adds a value to a Redis sorted set with a timestamp as its score.

        :param key: The Redis key pointing to the sorted set.
        :type  key: str
        :param value: The value to add to the sorted set.
        :type  value: str
        :param timestamp: The score used for sorting in the sorted set.
        :type  timestamp: int
        :returns: `True` if the sorted set existed before the addition, otherwise `False`.
        :rtype:   bool
        """
        is_exists_queue_and_add_wh_to_sorted_set = textwrap.dedent(
            """
            local is_exist_queue = redis.call('EXISTS', KEYS[1])
            redis.call('ZADD', KEYS[1], ARGV[1], ARGV[2])
            return is_exist_queue
            """
        )
        async with self._redis_dep.session() as session:
            is_exist = await session.eval(is_exists_queue_and_add_wh_to_sorted_set, 1, key, timestamp, value)
            return bool(is_exist)

    async def get_wh_sorted_list(self, key: str) -> list[str] | None:
        """
        Retrieves a sorted list from a Redis sorted set, deletes the set afterward.

        :param key: The Redis key pointing to the sorted set to retrieve.
        :type  key: str
        :returns: A list of sorted elements from the Redis sorted set, or None if no data was found.
        :rtype:   list[str] | None
        """
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
