from pydantic import BaseModel

from src.entities.schemas.base_data.base_schemas import IDSchema


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectSchema(IDSchema, ProjectCreateSchema):
    pass
