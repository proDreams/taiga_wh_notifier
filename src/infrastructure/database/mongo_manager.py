from bson import ObjectId

from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_types_schemas import ProjectTypeSchema
from src.entities.schemas.user_data.user_schemas import (
    GetAdminSchema,
    UserCreateSchema,
    UserSchema,
)
from src.infrastructure.database.mongo_dependency import MongoDBDependency


class MongoManager:
    """
    Manages interaction with MongoDB database.
    """

    def __init__(self, mongo_dep: MongoDBDependency) -> None:
        """
        Initializes an instance of the class with a MongoDBDependency.

        :param mongo_dep: The dependency object for MongoDB operations.
        :type mongo_dep: MongoDBDependency
        """
        self._mongo_dep = mongo_dep

    async def get_project_type_by_id(self, project_type_id: str) -> ProjectTypeSchema:
        """
        Retrieves the project type schema by its ID from the database.

        :param project_type_id: The unique identifier of the project type.
        :type project_type_id: str
        :return: The project type schema corresponding to the provided ID.
        :rtype: ProjectTypeSchema
        :raises ValueError: If no project type is found with the given ID.
        """
        async with self._mongo_dep.session() as session:
            collection = await self._mongo_dep.get_collection(DBCollectionEnum.project_type)
            document = await collection.find_one({"_id": ObjectId(project_type_id)}, session=session)

            if not document:
                raise ValueError(f"Project type with id {project_type_id} not found")

            return ProjectTypeSchema.model_validate(document, from_attributes=True)

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserSchema | None:
        """
        Fetches a user by their Telegram ID from the database.

        :param telegram_id: The unique identifier of the user in Telegram.
        :type telegram_id: int
        :returns: A `UserSchema` instance if a user with the given Telegram ID exists, otherwise `None`.
        :rtype: UserSchema | None
        """
        async with self._mongo_dep.session() as session:
            collection = await self._mongo_dep.get_collection(DBCollectionEnum.users)

            if document := await collection.find_one({"telegram_id": telegram_id}, session=session):
                return UserSchema.model_validate(document, from_attributes=True)

            return None

    async def create_user(self, user: UserCreateSchema) -> UserSchema:
        """
        Creates a new user in the database if the user with the provided Telegram ID does not exist.

        :param user: The user data to be created.
        :type user: UserCreateSchema
        :returns: The created or existing user schema.
        :rtype: UserSchema
        """
        if existing_user := await self.get_user_by_telegram_id(user.telegram_id):
            return existing_user

        async with self._mongo_dep.session() as session:
            collection = await self._mongo_dep.get_collection(DBCollectionEnum.users)
            result = await collection.insert_one(user.model_dump(mode="json"), session=session)

            inserted_document = await collection.find_one({"_id": result.inserted_id}, session=session)

            return UserSchema.model_validate(inserted_document)

    async def get_admins(self, offset: int, limit: int) -> tuple[list[GetAdminSchema], int]:
        async with self._mongo_dep.session() as session:
            filter_query = {"is_admin": True}

            collection = await self._mongo_dep.get_collection(DBCollectionEnum.users)
            result = await collection.find(filter_query, session=session).skip(offset).limit(limit)
            admins = [GetAdminSchema(**doc) async for doc in result]

            total_count = await collection.count_documents(filter_query)

            return admins, total_count
