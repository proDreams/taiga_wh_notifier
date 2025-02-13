import pytest
from redis.asyncio import Redis

from src.infrastructure.broker.redis_dependency import RedisSessionDependency


@pytest.mark.asyncio
class TestRedisSessionDependency:
    """
    Tests for the RedisSessionDependency class.
    """

    async def test_session_returns_redis_instance(self):
        """
        Tests that the session method returns a Redis instance.

        :raises AssertionError: If the returned object is not an instance of `Redis` or if the PING command returns False.
        """
        dependency = RedisSessionDependency()
        async with dependency.session() as redis_client:
            assert isinstance(redis_client, Redis)
            pong = await redis_client.ping()
            assert pong is True

    async def test_multiple_sessions_are_independent(self):
        """
        Tests that multiple Redis sessions are independent of each other.

        This test method creates two separate Redis session clients using the `RedisSessionDependency`
        and asserts that they are not the same object, demonstrating the independence of multiple sessions.
        """
        dependency = RedisSessionDependency()
        async with dependency.session() as client1:
            async with dependency.session() as client2:
                assert client1 is not client2
