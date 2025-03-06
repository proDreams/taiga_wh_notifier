from src.core.settings import get_settings
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_schemas import (
    ProjectCreateSchema,
    ProjectSchema,
)
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.infrastructure.database.mongo_manager import MongoManager


class ProjectService:
    """
    Service class for managing project operations
    """

    def __init__(self) -> None:
        """
        Initialize the project service.

        Initializes MongoDB connection and sets the working collection
        according to DBCollectionEnum.PROJECT.
        """
        self.mongo_manager = MongoManager(MongoDBDependency())
        self.collection = DBCollectionEnum.PROJECT

    async def get_projects(self, page: int) -> tuple[list[ProjectSchema], int]:
        """
        Retrieve paginated list of projects.

        :param page: Page number for pagination (0-based index)
        :type page: int
        :return: Tuple containing:
            - List of ProjectSchema objects
            - Total number of projects in database
        :rtype: tuple[list[ProjectSchema], int]
        """
        limit = get_settings().ITEMS_PER_PAGE
        offset = page * limit
        projects = await self.mongo_manager.find_with_limit(
            collection=self.collection,
            schema=ProjectSchema,
            offset=offset,
            limit=limit,
        )
        total_count = await self.mongo_manager.count_documents(
            collection=self.collection,
        )
        return (projects, total_count)

    async def get_project(self, project_id: str) -> ProjectSchema | None:
        """
        Find a project by its unique identifier.

        :param project_id: UUID of the project to find
        :type project_id: str
        :return: Found project or None if not found
        :rtype: ProjectSchema | None
        """
        return await self.mongo_manager.find_one(collection=self.collection, schema=ProjectSchema, value=project_id)

    async def get_or_create_project(self, name: str) -> tuple[ProjectSchema, bool]:
        """
        Create a new project or return existing one.

        :param name: Project name to search/create
        :type name: str
        :return: Tuple containing:
            - Project object (new or existing)
            - Creation flag (True if new project was created)
        :rtype: tuple[ProjectSchema, bool]
        """
        async with self.mongo_manager._get_session() as session:
            if existing_project := await self.mongo_manager.find_one(
                collection=self.collection,
                schema=ProjectSchema,
                field="name",
                value=name,
                session=session,
            ):
                return existing_project, False
            await self.mongo_manager.insert_one(
                collection=self.collection,
                data=ProjectCreateSchema(name=name),
                session=session,
            )
            new_project = await self.mongo_manager.find_one(
                collection=self.collection, schema=ProjectSchema, field="name", value=name, session=session
            )
            return new_project, True
