from fastapi import HTTPException, Path
from starlette import status

from src.entities.schemas.project_data.project_schemas import ProjectSchema
from src.logic.services.project_service import ProjectService


async def validate_instance(instance: str = Path(...)) -> ProjectSchema:
    """
    Validates the event type by fetching it from the MongoDB database.

    :param instance: The ID of the instance to validate.
    :type instance: str
    :returns: The ProjectSchema representing the validated project.
    :rtype: ProjectSchema
    :raises HTTPException: If the event type is not found in the database.
    """
    if project := await ProjectService().get_instance(instance_id=instance):
        return project

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Instance {instance} not found")
