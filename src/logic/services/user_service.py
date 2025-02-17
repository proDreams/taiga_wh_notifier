from src.entities.schemas.user_data.user_schemas import UserCreateSchema, UserSchema
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.infrastructure.database.mongo_manager import MongoManager


class UserService:
    def __init__(self):
        self.mongo_manager = MongoManager(MongoDBDependency())

    async def get_or_create_user(self, user: UserCreateSchema) -> UserSchema:
        return await self.mongo_manager.create_user(user=user)
