from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId

from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.infrastructure.database.mongo_manager import MongoManager


@pytest.mark.asyncio
class TestMongoManager:
    """
    Class for testing the MongoManager functionality.
    """

    @pytest.fixture(autouse=True)
    def setup_mongo_dep(self) -> None:
        """
        Sets up a mock dependency for MongoDB operations.

        This method creates and configures mock objects for session management,
        collection access, and database queries to facilitate unit testing without
        relying on an actual MongoDB instance.
        """
        fake_collection = MagicMock()
        fake_collection.find_one = AsyncMock()

        fake_session_cm = AsyncMock()
        fake_session_cm.__aenter__.return_value = "fake_session"
        fake_session_cm.__aexit__.return_value = None

        self.mongo_dep = MagicMock()
        self.mongo_dep.session.return_value = fake_session_cm
        self.mongo_dep.get_collection = AsyncMock(return_value=fake_collection)

    async def test_get_project_type_by_id_found(self) -> None:
        """
        Tests the functionality of getting a project type by its ID when it is found.

        :raises AssertionError: If any of the assertions fail, indicating that the method did not return the expected result.
        """
        valid_id = "507f1f77bcf86cd799439011"
        name = "example"
        document = {
            "id": ObjectId(valid_id),
            "name": name,
            "instances": [
                {
                    "_id": ObjectId(valid_id),
                    "fat": ["epic"],
                    "chat_id": 12345,
                    "thread_id": None,
                    "webhook_url": "33242",
                }
            ],
        }
        fake_collection = self.mongo_dep.get_collection.return_value
        fake_collection.find_one.return_value = document

        manager = MongoManager(mongo_dep=self.mongo_dep)

        result = await manager.find_one(collection=DBCollectionEnum.PROJECT_TYPE, schema=ProjectSchema, value=valid_id)

        assert isinstance(result, ProjectSchema)
        assert result.instances[0].fat == ["epic"]
        assert result.instances[0].chat_id == 12345
        assert result.instances[0].thread_id is None

    @pytest.mark.asyncio
    async def test_get_project_type_by_id_not_found(self) -> None:
        """
        Tests the behavior of the get_project_type_by_id method when an invalid project type ID is provided.

        :raises AssertionError: If any of the assertions fail, indicating that the method did not return the expected result.
        """
        invalid_id = "507f1f77bcf86cd799439012"
        fake_collection = self.mongo_dep.get_collection.return_value
        fake_collection.find_one.return_value = None

        manager = MongoManager(mongo_dep=self.mongo_dep)

        result = await manager.find_one(
            collection=DBCollectionEnum.PROJECT_TYPE, schema=ProjectSchema, value=invalid_id
        )

        assert result is None
