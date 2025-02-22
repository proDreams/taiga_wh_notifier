from src.core.settings import Configuration
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.infrastructure.database.mongo_manager import MongoManager


class ProjectService:
    def __init__(self) -> None:
        self.mongo_manager = MongoManager(MongoDBDependency())

    async def get_projects(self, page: int) -> tuple[list[ProjectSchema], int]:
        limit = Configuration.settings.ITEMS_PER_PAGE
        offset = page * limit

        return await self.mongo_manager.get_projects(limit=limit, offset=offset)

    async def get_project(self, project_id: str) -> ProjectSchema | None:
        return await self.mongo_manager.find_one(
            collection=DBCollectionEnum.PROJECT, schema=ProjectSchema, value=project_id
        )
