from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from src.entities.schemas.validators.project_validators import validate_object_id


class IDSchema(BaseModel):
    """
    Represents the schema for an identifier (ID) in a data model.

    :ivar id: A string representing the unique identifier of an object.
    :type id: str
    """

    id: Annotated[str, BeforeValidator(validate_object_id), Field(alias="_id")]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
