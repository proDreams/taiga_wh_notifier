from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from src.entities.enums.event_enums import EventTypeEnum
from src.entities.enums.lang_enum import LanguageEnum
from src.entities.schemas.base_data.base_schemas import IDSchema
from src.entities.schemas.validators.project_validators import validate_object_id


class InstanceCreateModel(BaseModel):
    """
    Represents the schema for instance

    :ivar fat: Following Action Type object
    :type fat: list[EventTypeEnum]
    :ivar chat_id: Unique identifier for the telegram chat
    :type chat_id: int
    :ivar thread_id: Unique identifier for the telegram superchat
    :type thread_id: int | None
    :ivar webhook_url: url for webhook of taiga
    :type webhook_url: str | None
    :ivar language: Option for language of telegram notifications
    :type language: LanguageEnum
    """

    instance_id: Annotated[str, BeforeValidator(validate_object_id), Field(alias="instance_id")]

    instance_name: str
    project_id: str
    fat: list[EventTypeEnum] = []
    chat_id: int | None = None
    thread_id: int | None = None
    webhook_url: str | None = None
    language: LanguageEnum

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class InstanceModel(InstanceCreateModel):
    pass


class ProjectCreateSchema(BaseModel):
    """
    Represents the schema for creating a project.

    :ivar name: Name of the project to be created.
    :type name: str
    :ivar instances: A list of instances associated with the project.
        Each instance is represented by the `InstanceModel` schema, which includes
        details such as the following action type (FAT), chat ID, thread ID, and
        webhook URL. Defaults to an empty list if no instances are provided.
    :type instances: List[InstanceModel]
    """

    name: str
    instances: list[InstanceModel] = []


class ProjectSchema(IDSchema, ProjectCreateSchema):
    """
    Class for representing a project schema.

    :ivar id: The unique identifier of the project.
    :type id: str (inherited from ISchema)
    :ivar name: Name of the project.
    :type name: str (inherited from ISchema)
    """

    pass
