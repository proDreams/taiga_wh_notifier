from unittest.mock import AsyncMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from motor.motor_asyncio import AsyncIOMotorClientSession

from src.infrastructure.database.mongo_dependency import MongoDBDependency


@pytest.mark.asyncio
class TestMongoDBDependency:
    """
    Tests the functionality of MongoDBDependency class for managing MongoDB sessions.
    """

    @pytest.fixture
    def dummy_session(self) -> AsyncMock:
        """
        Provides a dummy session for testing purposes.

        :return: An asynchronous mock of an AsyncIOMotorClientSession.
        :rtype: AsyncIOMotorClientSession
        """
        session = AsyncMock(spec=AsyncIOMotorClientSession)
        session.end_session = AsyncMock()
        return session

    @pytest.fixture
    def mongo_dep(
        self, monkeypatch: MonkeyPatch, dummy_session: AsyncMock
    ) -> tuple[MongoDBDependency, AsyncMock, AsyncMock]:
        """
        Provides a fixture for mocking the MongoDB dependency in tests.

        :param monkeypatch: A pytest fixture that allows patching objects during testing.
        :type monkeypatch: MonkeyPatch
        :param dummy_session: An asynchronous mock object representing a MongoDB session.
        :type dummy_session: AsyncMock

        :returns: A tuple containing the mocked MongoDBDependency instance, the dummy session, and the start_session mock.
        :rtype: Tuple[MongoDBDependency, AsyncMock, AsyncMock]
        """
        mongo_dep = MongoDBDependency()
        start_session_mock = AsyncMock(return_value=dummy_session)
        monkeypatch.setattr(mongo_dep._client, "start_session", start_session_mock)
        return mongo_dep, dummy_session, start_session_mock

    async def test_session_returns_correct_session(
        self, mongo_dep: tuple[MongoDBDependency, AsyncMock, AsyncMock]
    ) -> None:
        """
        Tests the functionality of the session returned by MongoDBDependency.

        :param mongo_dep: A tuple containing the MongoDBDependency instance and two mock objects for session management.
        :type mongo_dep: tuple[MongoDBDependency, AsyncMock, AsyncMock]
        :raises AssertionError: If the obtained session is not the dummy_session or if end_session is not called correctly.
        """
        mongo_dep, dummy_session, start_session_mock = mongo_dep

        async with mongo_dep.session() as session:
            assert session is dummy_session
            dummy_session.end_session.assert_not_called()

        dummy_session.end_session.assert_awaited_once()
        start_session_mock.assert_awaited_once()

    async def test_end_session_called_after_context_exit(
        self, mongo_dep: tuple[MongoDBDependency, AsyncMock, AsyncMock]
    ):
        """
        Tests whether the end_session method is called when the context manager exits.

        :param mongo_dep: A tuple containing a MongoDBDependency instance and two AsyncMock instances for mocking session methods.
        :type mongo_dep: tuple[MongoDBDependency, AsyncMock, AsyncMock]
        :raises AssertionError: If end_session is not awaited exactly once after exiting the context manager.
        """
        mongo_dep, dummy_session, _ = mongo_dep

        async with mongo_dep.session():
            pass

        dummy_session.end_session.assert_awaited_once()
