from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.base_data.base_schemas import IDSchema
from src.entities.schemas.validators.project_validators import validate_object_id


class ProjectTypeCreateSchema(BaseModel):
    """
    Schema for creating a project type.

    :ivar event_type: Type of the event related to the project.
    :type event_type: EventTypeEnum
    :ivar chat_id: ID or list of IDs of the chat associated with the project.
    :type chat_id: int | list[int]
    :ivar thread_id: Optional ID or list of IDs of the thread associated with the project.
    :type thread_id: int | list[int] | None = None
    :ivar project_id: Annotated string representing the unique identifier of the project, validated before use.
    :type project_id: Annotated[str, BeforeValidator(validate_object_id)]
    """

    event_type: EventTypeEnum
    chat_id: int | list[int]
    thread_id: int | list[int] | None = None
    project_id: Annotated[str, BeforeValidator(validate_object_id)]


class ProjectTypeSchema(IDSchema, ProjectTypeCreateSchema):
    """
    Represents the schema for project types, extending both ISchema and ProjectTypeCreateSchema.

    :ivar id: Unique identifier of the project type.
    :type id: str
    :ivar event_type: Type of the event related to the project.
    :type event_type: EventTypeEnum
    :ivar chat_id: ID or list of IDs of the chat associated with the project.
    :type chat_id: int | list[int]
    :ivar thread_id: Optional ID or list of IDs of the thread associated with the project.
    :type thread_id: int | list[int] | None = None
    :ivar project_id: Annotated string representing the unique identifier of the project, validated before use.
    :type project_id: Annotated[str, BeforeValidator(validate_object_id)]
    """

    pass
