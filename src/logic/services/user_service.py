from aiogram.types import SharedUser, User
from bson import ObjectId

from src.core.settings import get_settings
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.user_data.user_schemas import (
    GetAdminSchema,
    UserCreateSchema,
    UserSchema,
)
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.infrastructure.database.mongo_manager import MongoManager
from src.utils.text_utils import generate_admins_text


class UserService:
    """
    Service class for managing user operations.

    This class provides methods to interact with the user database using a MongoDB manager.
    """

    def __init__(self) -> None:
        """
        Initializes an instance of the class.

        :param self.mongo_manager: An instance of MongoManager.
        :type self.mongo_manager: MongoManager
        """
        self.mongo_manager = MongoManager(MongoDBDependency())
        self.collection = DBCollectionEnum.USERS

    async def get_or_create_user(self, user: User) -> UserSchema:
        """
        Retrieve or create a user in the database.

        :param user: User instance to be processed.
        :type user: User
        :returns: The created or existing user data.
        :rtype: UserSchema
        """
        user_obj = UserCreateSchema(
            **user.model_dump(), telegram_id=user.id, is_admin=user.id in get_settings().ADMIN_IDS
        )

        return await self.mongo_manager.create_user(
            collection=self.collection, insert_data=user_obj, return_schema=UserSchema
        )

    async def get_admins(self, page: int) -> tuple[list[GetAdminSchema], int]:
        limit = get_settings().ITEMS_PER_PAGE
        offset = page * limit

        pipeline = [
            {"$match": {"is_admin": True}},
            {
                "$facet": {
                    "items": [
                        {"$skip": offset},
                        {"$limit": limit},
                    ],
                    "total": [{"$count": "count"}],
                }
            },
        ]

        return await self.mongo_manager.aggregate(
            pipeline=pipeline, collection=self.collection, schema=GetAdminSchema, item_key="items"
        )

    async def get_user(self, user_id: str) -> UserSchema | None:
        """
        Asynchronously retrieves a user by their ID from the database.

        :param user_id: The unique identifier for the user.
        :type user_id: str
        :returns: A UserSchema object if the user is found, otherwise None.
        :rtype: UserSchema | None
        """
        return await self.mongo_manager.find_one_by_id(collection=self.collection, schema=UserSchema, value=user_id)

    async def update_user(self, user_id: str, field: str, value: str | int | bool) -> None:
        """
        Updates a user's information in the database.

        :param user_id: The unique identifier of the user to be updated.
        :type user_id: str
        :param field: The field name that needs to be updated.
        :type field: str
        :param value: The new value for the specified field.
        :type value: str | int | bool
        """
        return await self.mongo_manager.update_one(
            collection=self.collection,
            filter_field="_id",
            filter_value=ObjectId(user_id),
            update_field=field,
            update_value=value,
        )

    async def save_admins(self, users: list[SharedUser]) -> tuple[str | None, str | None]:
        """
        Saves a list of users as administrators in the database.

        :param users: List of SharedUser objects to be saved as administrators.
        :type users: list[SharedUser]
        :returns: A tuple containing two strings - success message and error message.
        :rtype: tuple[str, str]
        """
        users_list = [
            UserCreateSchema(**user.model_dump(), telegram_id=user.user_id, is_admin=True)
            for user in users
            if await self.mongo_manager.find_one(
                collection=self.collection, schema=UserSchema, value=user.user_id, field="telegram_id"
            )
            is None
        ]

        if users_list:
            await self.mongo_manager.insert_many(collection=self.collection, data_list=users_list)

            return await generate_admins_text(admins_list=users_list)

        return None, None
