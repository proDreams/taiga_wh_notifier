from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.infrastructure.broker.redis_manager import RedisManager


@pytest.mark.asyncio
class TestRedisManager:
    """
    Class for managing Redis operations in an asynchronous manner.
    """

    class _FakeContextManager:
        """
        A fake context manager class used for testing purposes.

        This class mimics the behavior of a context manager by returning an `AsyncMock` session
        in the `__aenter__` method and doing nothing in the `__aexit__` method. It is designed
        to be used in asynchronous code where you need to mock or simulate a context manager.
        """

        def __init__(self, session: AsyncMock) -> None:
            """
            Initializes a new instance of the class.

            :param session: An asynchronous mock object for session management.
            :type session: AsyncMock
            """
            self.session: AsyncMock = session

        async def __aenter__(self) -> AsyncMock:
            return self.session

        async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
            pass

    @pytest.fixture
    def fake_session(self) -> AsyncMock:
        """
        Provides a fixture for creating a fake asynchronous session.

        :return: An instance of AsyncMock representing a fake asynchronous session.
        :rtype: AsyncMock
        """
        return AsyncMock()

    @pytest.fixture
    def fake_redis_dep(self, fake_session: AsyncMock) -> MagicMock:
        """
        Provides a fixture for simulating Redis dependency in tests.

        :returns: A MagicMock object configured to simulate a Redis session.
        :rtype: MagicMock
        """
        fake_dep: MagicMock = MagicMock()
        fake_dep.session.return_value = self._FakeContextManager(fake_session)
        return fake_dep

    @pytest.fixture
    def redis_manager(self, fake_redis_dep: MagicMock) -> RedisManager:
        """
        Returns an instance of RedisManager configured with a fake Redis dependency.

        :param fake_redis_dep: A MagicMock object representing the fake Redis dependency.
        :type fake_redis_dep: MagicMock
        :returns: An instance of RedisManager initialized with the provided fake Redis dependency.
        :rtype: RedisManager
        """
        return RedisManager(redis_dep=fake_redis_dep)

    async def test_set_data(self, redis_manager: RedisManager, fake_session: AsyncMock) -> None:
        """
        Tests the set_data method of RedisManager by verifying that it correctly sets data in Redis and fake_session.

        :param redis_manager: Instance of RedisManager responsible for managing Redis operations.
        :type redis_manager: RedisManager
        :param fake_session: Mock object representing a session used to simulate database operations.
        :type fake_session: AsyncMock
        :raises AssertionError: If the set_data method does not correctly interact with fake_session or if the expected data is not retrieved.
        """
        key: str = "test_key"
        value: str = "test_value"

        await redis_manager.set_data(key, value)

        fake_session.set.assert_awaited_once_with(key, value)

    async def test_delete_data(self, redis_manager: RedisManager, fake_session: AsyncMock) -> None:
        """
        Tests the deletion of data from a Redis database and session.

        :param redis_manager: Instance of RedisManager used for interacting with Redis.
        :type redis_manager: RedisManager
        :param fake_session: Mock object representing an asynchronous session interface.
        :type fake_session: AsyncMock
        :raises AssertionError: If the delete_data method does not execute as expected.
        """
        key: str = "test_key"

        await redis_manager.delete_data(key)

        fake_session.delete.assert_awaited_once_with(key)
