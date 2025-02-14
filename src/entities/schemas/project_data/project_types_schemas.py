from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.project_data.base_project_schemas import ProjectIDSchema
from src.entities.schemas.validators.project_validators import validate_object_id


class ProjectTypeCreateSchema(BaseModel):
    event_type: EventTypeEnum
    chat_id: int | list[int]
    thread_id: int | list[int] | None = None
    project_id: Annotated[str, BeforeValidator(validate_object_id)]


class ProjectTypeSchema(ProjectIDSchema, ProjectTypeCreateSchema):
    pass
