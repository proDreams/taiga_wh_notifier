from bson import ObjectId

from src.core.settings import get_logger, get_settings
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.project_data.project_schemas import (
    InstanceCreateModel,
    InstanceModel,
    ProjectCreateSchema,
    ProjectSchema,
)
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.infrastructure.database.mongo_manager import MongoManager

logger = get_logger(name=__name__)


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
        logger.info(f"projects: {projects}")
        total_count = await self.mongo_manager.count_documents(collection=self.collection, filter_query={})
        return projects, total_count

    async def get_project(self, project_id: str) -> ProjectSchema | None:
        """
        Find a project by its unique identifier.

        :param project_id: UUID of the project to find
        :type project_id: str
        :return: Found project or None if not found
        :rtype: ProjectSchema | None
        """
        return await self.mongo_manager.find_one_by_id(
            collection=self.collection, schema=ProjectSchema, value=project_id
        )

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
                collection=self.collection,
                schema=ProjectSchema,
                field="name",
                value=name,
                session=session,
            )
            return new_project, True

    async def update_project_name(self, project_id: str, new_name: str):
        result = await self.mongo_manager.update_one(
            collection=self.collection,
            filter_field="_id",
            filter_value=ObjectId(project_id),
            update_field="name",
            update_value=new_name,
        )
        return result

    async def add_new_instance(
        self,
        new_instance: InstanceCreateModel,
        name: str = None,
        project_id: str = None,
    ):
        if name:
            project, created = await self.get_or_create_project(name=name)
            project_id = project.id
        elif project_id:
            pass
        else:
            raise ValueError("name or project_id must defined")
        async with self.mongo_manager._get_session() as session:
            collection = await self.mongo_manager._get_collection(collection=self.collection)
            data = new_instance.model_dump()
            data["instance_id"] = ObjectId()
            data["project_id"] = str(project_id)
            result = await collection.update_one(
                {"_id": ObjectId(project_id)},
                {"$push": {"instances": data}},
                session=session,
            )
            return result

    async def get_paginated_instances(self, project_id, page: int) -> tuple[list[InstanceModel], int]:
        limit = get_settings().ITEMS_PER_PAGE
        offset = page * limit
        project = await self.get_project(project_id=project_id)
        if not project:
            raise ValueError(f"project {project_id} is not found")
        instances = project.instances
        if not instances:
            return [], 0
        paginated_instances = instances[offset : offset + limit]
        return paginated_instances, len(instances)

    async def get_instance(self, project_id, instance_id: str):
        project = await self.get_project(project_id=project_id)
        if not project:
            raise ValueError(f"project {project_id} is not found")
        instance = list(filter(lambda x: str(x.instance_id) == instance_id, project.instances))[0]
        if not instance:
            raise ValueError(f"instance {instance_id} not found")
        return instance

    async def update_instance_fat(self, project_id, instance_id: str, fat: list[EventTypeEnum]):
        project = await self.get_project(project_id=project_id)
        updated = False
        new_instances = []
        for instance in project.instances:
            if str(instance.instance_id) == instance_id:
                if instance.fat != fat:
                    updated = True
                    instance.fat = fat
                    new_instances.append(instance.model_dump())
                else:
                    break
            else:
                new_instances.append(instance.model_dump())
        if updated:
            async with self.mongo_manager._get_session() as session:
                collection = await self.mongo_manager._get_collection(collection=self.collection)
                return await collection.update_one(
                    {"_id": ObjectId(project_id)}, {"$set": {"instances": new_instances}}, session=session
                )
        return None

    async def delete_project(self, project_id: str) -> None:
        return await self.mongo_manager.delete_one_by_id(
            collection=self.collection,
            value=project_id,
        )

    async def get_instance_by_name(self, project_id: str, instance_name: str) -> InstanceModel | None:
        project = await self.get_project(project_id=project_id)
        for inst in project.instances:
            if inst.instance_name == instance_name:
                return inst
        return None

    async def update_instance(self, project_id: str, instance_id: str, field: str, value):
        project = await self.get_project(project_id=project_id)
        if not project_id:
            raise ValueError(f"project {project_id} is not found")
        updated = False
        new_instances = []

        for instance in project.instances:
            if str(instance.instance_id) == instance_id:
                updated_instance = instance.model_copy()
                setattr(updated_instance, field, value)
                new_instances.append(updated_instance.model_dump())
                updated = True
            else:
                new_instances.append(instance.model_dump())

        if updated:
            data = new_instances
            async with self.mongo_manager._get_session() as session:
                collection = await self.mongo_manager._get_collection(collection=self.collection)
                return await collection.update_one(
                    {"_id": ObjectId(project_id)},
                    {"$set": {"instances": data}},
                    session=session,
                )
        return None

    async def get_fat_list(self, project_id: str, instance_id: str) -> list[EventTypeEnum]:
        instance = await self.get_instance(project_id=project_id, instance_id=instance_id)
        return instance.fat
