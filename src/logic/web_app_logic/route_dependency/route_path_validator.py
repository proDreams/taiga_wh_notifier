from fastapi import Depends, HTTPException, Path
from starlette import status

from src.entities.enums.collection_enum import DBCollectionEnum
from src.entities.schemas.project_data.project_types_schemas import ProjectTypeSchema
from src.infrastructure.database.mongo_manager import MongoManager
from src.logic.web_app_logic.route_dependency.mongo_dependency import get_mongo_manager


async def validate_event_type(
    event_type: str = Path(...), mongo_manager: MongoManager = Depends(get_mongo_manager)
) -> ProjectTypeSchema:
    """
    Validates the event type by fetching it from the MongoDB database.

    :param event_type: The ID of the project type to validate.
    :type event_type: str
    :mongo_manager: Instance of the MongoManager to interact with the database.
    :type mongo_manager: MongoManager
    :returns: The ProjectTypeSchema representing the validated event type.
    :rtype: ProjectTypeSchema
    :raises HTTPException: If the event type is not found in the database.
    """
    if result := await mongo_manager.find_one(
        collection=DBCollectionEnum.PROJECT_TYPE, value=event_type, schema=ProjectTypeSchema
    ):
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project type {event_type} not found")
