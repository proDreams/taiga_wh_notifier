from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from src.core.Base.singleton import Singleton
from src.core.settings import Configuration


class MongoDBDependency(Singleton):
    """
    Manages dependencies for MongoDB operations within a Singleton pattern.

    This class ensures that only one instance of the MongoDB connection is created and reused throughout the application.
    It provides an asynchronous context manager for managing database sessions, which simplifies transaction management.
    """

    def __init__(self) -> None:
        """
        Initialize the database connection for the application.

        This method sets up an asynchronous MongoDB client using `AsyncIOMotorClient` and connects to a specified database.
        It retrieves the database URL and name from the application's configuration settings and establishes the connection to be used throughout the application.
        """
        self._client = AsyncIOMotorClient(Configuration.settings.DB_URL)
        self._db = self._client[Configuration.settings.DB_NAME]

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncIOMotorClientSession, None]:
        """
        Manages the lifecycle of an asynchronous MongoDB session.

        :returns: AsyncGenerator yielding a MotorClientSession instance.
        :rtype: AsyncGenerator[AsyncIOMotorClientSession, None]
        """
        session = await self._client.start_session()

        yield session

        await session.end_session()
