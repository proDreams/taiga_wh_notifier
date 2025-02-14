from pydantic import BaseModel

from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.project_data.base_project_schemas import ProjectIDSchema


class BaseProjectTypeSchema(BaseModel):
    type: EventTypeEnum
    chat_id: int | list[int]
    thread_id: int | list[int] | None = None


class TestSchema(ProjectIDSchema, BaseProjectTypeSchema):
    pass


class MilestoneSchema(ProjectIDSchema, BaseProjectTypeSchema):
    pass


class UserStorySchema(ProjectIDSchema, BaseProjectTypeSchema):
    pass


class TaskSchema(ProjectIDSchema, BaseProjectTypeSchema):
    pass


class IssueSchema(ProjectIDSchema, BaseProjectTypeSchema):
    pass
