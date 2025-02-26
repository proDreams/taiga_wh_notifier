from aiogram.types import User

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
        """
        Fetches or creates a user in the database.

        :param user: The user data to be fetched or created.
        :type user: UserCreateSchema
        :return: The user data from the database.
        :rtype: UserSchema
        """
        user_obj = UserCreateSchema(
            **user.model_dump(), telegram_id=user.id, is_admin=user.id in Configuration.settings.ADMIN_IDS
        )

        return await self.mongo_manager.create_user(
            collection=DBCollectionEnum.USERS, insert_data=user_obj, return_schema=UserSchema
        )

    async def get_admins(self, page: int) -> tuple[list[GetAdminSchema], int]:
        limit = Configuration.settings.ITEMS_PER_PAGE
        offset = page * limit

        return await self.mongo_manager.get_admins(limit=limit, offset=offset)

    async def get_user(self, user_id: str) -> UserSchema | None:
        return await self.mongo_manager.find_one(collection=DBCollectionEnum.USERS, schema=UserSchema, value=user_id)

    async def update_user(self, user_id: str, field: str, value: str | int | bool) -> None:
        return await self.mongo_manager.update_one(
            collection=DBCollectionEnum.USERS,
            filter_field="_id",
            filter_value=user_id,
            update_field=field,
            update_value=value,
        )
