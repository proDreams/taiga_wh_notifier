from fastapi import Depends

from src.infrastructure.database.mongo_dependency import MongoDBDependency, get_mongo_db
from src.infrastructure.database.mongo_manager import MongoManager


async def get_mongo_manager(mongo_db: MongoDBDependency = Depends(get_mongo_db)) -> MongoManager:
    """
    Returns an instance of the MongoManager class for managing MongoDB operations.

    :param mongo_db: A dependency injection object for MongoDB database connection.
    :type mongo_db: MongoDBDependency
    :returns: An instance of MongoManager configured with the provided MongoDB connection.
    :rtype: MongoManager
    """
    return MongoManager(mongo_db)
