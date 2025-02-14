from bson import ObjectId
from fastapi import Depends

from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_types_schemas import ProjectTypeSchema
from src.infrastructure.database.mongo_dependency import MongoDBDependency


class MongoManager:
    """
    Manages interaction with MongoDB database.
    """

    def __init__(self, mongo_dep: MongoDBDependency = Depends(MongoDBDependency)) -> None:
        """
        Initializes an instance of the class with a MongoDB dependency.

        :param mongo_dep: A dependency injected for MongoDB operations.
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
