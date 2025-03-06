from pydantic import BaseModel

from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.base_data.base_schemas import IDSchema


class FATModel(BaseModel):
    """
    Represents the schema for Following Action Type
    """

    epic: bool = False
    milestone: bool = False
    userstory: bool = False
    task: bool = False
    issue: bool = False
    wikipage: bool = False
    test: bool = False


class InstanceCreateModel(BaseModel):
    """
    Represents the schema for instance

    :ivar fat: Following Action Type object
    :type fat: FATModel
    :ivar chat_id: Unique identifier for the telegram chat
    :type chat_id: int
    :ivar thread_id: Unique identifier for the telegram superchat
    :type thread_id: int | None
    :ivar webhook_url: url for webhook of taiga
    :type webhook_url: str | None
    """

    fat: list[EventTypeEnum] = []
    chat_id: int
    thread_id: int | None = None
    webhook_url: str | None = None


class InstanceModel(IDSchema, InstanceCreateModel):
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
