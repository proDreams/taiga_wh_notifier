from pydantic import BaseModel

from src.entities.schemas.project_data.base_project_schemas import ProjectIDSchema


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectSchema(ProjectIDSchema, ProjectCreateSchema):
    pass
