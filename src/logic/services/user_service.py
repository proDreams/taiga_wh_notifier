from src.core.settings import Configuration
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

    async def get_or_create_user(self, user: UserCreateSchema) -> UserSchema:
        """
        Fetches or creates a user in the database.

        :param user: The user data to be fetched or created.
        :type user: UserCreateSchema
        :return: The user data from the database.
        :rtype: UserSchema
        """
        return await self.mongo_manager.create_user(user=user)

    async def get_admins(self, page: int) -> tuple[list[GetAdminSchema], int]:
        limit = Configuration.settings.ITEMS_PER_PAGE
        offset = page * limit

        return await self.mongo_manager.get_admins(limit=limit, offset=offset)
