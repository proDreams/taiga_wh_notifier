from pydantic import BaseModel

from src.entities.schemas.base_data.base_schemas import IDSchema


class ProjectCreateSchema(BaseModel):
    """
    Represents the schema for creating a project.

    :ivar name: Name of the project to be created.
    :type name: str
    """

    name: str


class ProjectSchema(IDSchema, ProjectCreateSchema):
    """
    Class for representing a project schema.

    :ivar id: The unique identifier of the project.
    :type id: str (inherited from ISchema)
    :ivar name: Name of the project.
    :type name: str (inherited from ISchema)
    """

    pass
