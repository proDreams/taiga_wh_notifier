from aiogram.types import User
from bson import ObjectId

from src.core.settings import Configuration
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.user_data.user_schemas import (
    GetAdminSchema,
    UserCreateSchema,
    UserSchema,
)
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.infrastructure.database.mongo_manager import MongoManager


class UserService:
    """
    Service class for managing user operations.

    This class provides methods to interact with the user database using a MongoDB manager.
    """

    def __init__(self) -> None:
        self.mongo_manager = MongoManager(MongoDBDependency())

    async def get_or_create_user(self, user: User) -> UserSchema:
        user_obj = UserCreateSchema(
            **user.model_dump(), telegram_id=user.id, is_admin=user.id in Configuration.settings.ADMIN_IDS
        )

        return await self.mongo_manager.create_user(
            collection=DBCollectionEnum.USERS, insert_data=user_obj, return_schema=UserSchema
        )

    async def get_admins(self, page: int) -> tuple[list[GetAdminSchema], int]:
        limit = Configuration.settings.ITEMS_PER_PAGE
        offset = page * limit
        filter_query = {"is_admin": True}

        admins = await self.mongo_manager.find_with_limit(
            collection=DBCollectionEnum.USERS,
            schema=GetAdminSchema,
            offset=offset,
            limit=limit,
            filter_query=filter_query,
        )
        count = await self.mongo_manager.count_documents(collection=DBCollectionEnum.USERS, filter_query=filter_query)

        return admins, count

    async def get_user(self, user_id: str) -> UserSchema | None:
        return await self.mongo_manager.find_one_by_id(
            collection=DBCollectionEnum.USERS, schema=UserSchema, value=user_id
        )

    async def update_user(self, user_id: str, field: str, value: str | int | bool) -> None:
        return await self.mongo_manager.update_one(
            collection=DBCollectionEnum.USERS,
            filter_field="_id",
            filter_value=ObjectId(user_id),
            update_field=field,
            update_value=value,
        )
