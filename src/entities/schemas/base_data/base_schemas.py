from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from src.entities.schemas.validators.project_validators import validate_object_id


class IDSchema(BaseModel):
    id: Annotated[str, BeforeValidator(validate_object_id), Field(alias="_id")]

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
