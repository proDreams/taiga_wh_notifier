from fastapi import Depends

from src.infrastructure.database.mongo_dependency import MongoDBDependency, get_mongo_db
from src.infrastructure.database.mongo_manager import MongoManager


async def get_mongo_manager(mongo_db: MongoDBDependency = Depends(get_mongo_db)) -> MongoManager:
    return MongoManager(mongo_db)
