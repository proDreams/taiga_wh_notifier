from aiogram.types import SharedUser, User
from bson import ObjectId

from src.core.settings import get_settings
from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.named_tuples.mongo_tuples import AggregateTuple
from src.entities.named_tuples.utils_tuples import AdminStrTuple
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
            **user.model_dump(),
            telegram_id=user.id,
            is_admin=user.id in get_settings().ADMIN_IDS,
        )

        return await self.mongo_manager.create_user(
            collection=self.collection, insert_data=user_obj, return_schema=UserSchema
        )

    async def get_admins(self, page: int) -> AggregateTuple:
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
            pipeline=pipeline,
            collection=self.collection,
            schema=GetAdminSchema,
            item_key="items",
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

    async def save_admins(self, users: list[SharedUser]) -> AdminStrTuple:
        """
        Promotes the supplied Telegram users to administrators, creating new records
        where necessary and updating existing ones.

        :param users: Telegram users shared via ``RequestUsers`` to be granted admin
                      rights.
        :type  users: list[SharedUser]

        :returns: ``AdminStrTuple`` where **admins_text** is a formatted
                  string for the confirmation message and **bot_link** is a deep
                  link to the bot; returns ``AdminStrTuple(None, None)`` if no users were added
                  or promoted.
        :rtype:   AdminStrTuple
        """
        new_admins: list[UserCreateSchema] = []
        promoted_admins: list[UserSchema] = []
        already_admins: list[UserSchema] = []

        for u in users:
            existing = await self.mongo_manager.find_one(
                collection=self.collection,
                schema=UserSchema,
                value=u.user_id,
                field="telegram_id",
            )

            if existing is None:
                new_admins.append(UserCreateSchema(**u.model_dump(), telegram_id=u.user_id, is_admin=True))
            else:
                if not existing.is_admin:
                    await self.mongo_manager.update_one(
                        collection=self.collection,
                        filter_field="telegram_id",
                        filter_value=u.user_id,
                        update_field="is_admin",
                        update_value=True,
                    )
                    promoted_admins.append(existing)
                else:
                    already_admins.append(existing)

        if new_admins:
            await self.mongo_manager.insert_many(collection=self.collection, data_list=new_admins)

        changed_admins = [*new_admins, *promoted_admins]

        if changed_admins:
            return await generate_admins_text(admins_list=changed_admins)

        return AdminStrTuple()
