from bson import ObjectId

from src.core.settings import get_settings
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.enums.lang_enum import LanguageEnum
from src.entities.named_tuples.mongo_tuples import AggregateTuple
from src.entities.schemas.project_data.project_schemas import (
    InstanceCreateModel,
    InstanceModel,
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
        self.limit = get_settings().ITEMS_PER_PAGE

    async def create_indexes(self) -> None:
        await self.mongo_manager.create_indexes()

    async def get_projects(self, page: int) -> AggregateTuple:
        offset = page * self.limit

        pipeline = [
            {
                "$facet": {
                    "items": [
                        {"$skip": offset},
                        {"$limit": self.limit},
                    ],
                    "total": [{"$count": "count"}],
                }
            }
        ]

        return await self.mongo_manager.aggregate(
            pipeline=pipeline, collection=self.collection, schema=ProjectSchema, item_key="items"
        )

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

    async def create_project(self, name: str) -> ProjectSchema:
        created_project = await self.mongo_manager.insert_one(
            collection=self.collection,
            data=ProjectCreateSchema(name=name),
        )

        new_project = await self.mongo_manager.find_one(
            collection=self.collection,
            schema=ProjectSchema,
            value=created_project.inserted_id,
        )

        return new_project

    async def update_project_name(self, project_id: str, new_name: str) -> None:
        await self.mongo_manager.update_one(
            collection=self.collection,
            filter_field="_id",
            filter_value=ObjectId(project_id),
            update_field="name",
            update_value=new_name,
        )

    async def add_new_instance(self, instance_name: str, lang: str, project_id: str) -> str:
        instance = InstanceCreateModel(
            instance_name=instance_name, language=LanguageEnum(lang), project_id=project_id, instance_id=str(ObjectId())
        )

        await self.mongo_manager.update_custom(
            collection=self.collection,
            filter_field="_id",
            filter_value=ObjectId(project_id),
            update_field="instances",
            update_value=instance.model_dump(mode="json"),
            command="$push",
        )

        return str(instance.instance_id)

    async def get_paginated_instances(self, project_id, page: int) -> AggregateTuple:
        offset = page * self.limit

        pipeline = [
            {"$match": {"_id": ObjectId(project_id)}},  # Убедитесь, что передаете правильный ObjectId
            {
                "$project": {
                    "instances": {"$slice": ["$instances", offset, self.limit]},
                    "total": {"$size": "$instances"},
                }
            },
        ]

        return await self.mongo_manager.aggregate(
            pipeline=pipeline, collection=self.collection, schema=InstanceModel, item_key="instances"
        )

    async def get_instance(self, instance_id: str) -> ProjectSchema | None:
        pipeline = [
            {"$match": {"instances.instance_id": instance_id}},
            {
                "$project": {
                    "instances": {
                        "$filter": {
                            "input": "$instances",
                            "as": "instance",
                            "cond": {"$eq": ["$$instance.instance_id", instance_id]},
                        }
                    },
                    "name": 1,
                    "_id": 1,
                }
            },
            {"$group": {"_id": None, "items": {"$push": {"instances": "$instances", "name": "$name", "_id": "$_id"}}}},
        ]

        document_list, total = await self.mongo_manager.aggregate(
            pipeline=pipeline,
            collection=self.collection,
            schema=ProjectSchema,
            item_key="items",
        )

        return document_list[0]

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

    async def update_instance(
        self, instance_id: str, update_field: str, update_value: str | int | bool | list[str]
    ) -> None:
        await self.mongo_manager.update_custom(
            collection=self.collection,
            filter_field="instances.instance_id",
            filter_value=instance_id,
            update_field=f"instances.$.{update_field}",
            update_value=update_value,
            command="$set",
        )

    async def delete_instance(self, instance_id: str) -> None:
        await self.mongo_manager.update_custom(
            collection=self.collection,
            filter_field="instances.instance_id",
            filter_value=instance_id,
            update_field="instances",
            update_value={"instance_id": instance_id},
            command="$pull",
        )

    async def get_fat_list(self, instance_id: str) -> list[EventTypeEnum]:
        project = await self.get_instance(instance_id=instance_id)

        # always one element
        return project.instances[0].fat
