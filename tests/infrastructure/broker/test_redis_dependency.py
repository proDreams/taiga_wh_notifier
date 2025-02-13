import pytest
from redis.asyncio import Redis

from src.infrastructure.broker.redis_dependency import RedisSessionDependency


@pytest.mark.asyncio
class TestRedisSessionDependency:
    async def test_session_returns_redis_instance(self):
        dependency = RedisSessionDependency()
        async with dependency.session() as redis_client:
            assert isinstance(redis_client, Redis)
            pong = await redis_client.ping()
            assert pong is True

    async def test_multiple_sessions_are_independent(self):
        dependency = RedisSessionDependency()
        async with dependency.session() as client1:
            async with dependency.session() as client2:
                assert client1 is not client2
