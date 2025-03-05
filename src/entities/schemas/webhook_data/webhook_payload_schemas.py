from datetime import datetime

from pydantic import BaseModel, field_validator

from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.webhook_data.diff_webhook_schemas import Change
from src.entities.schemas.webhook_data.nested_schemas import (
    Epic,
    Issue,
    Milestone,
    Task,
    User,
    UserStory,
    Wiki,
)


class WebhookPayload(BaseModel):
    action: str
    type: EventTypeEnum
    by: User
    date: datetime
    data: Task | Milestone | UserStory | Epic | Wiki | Issue
    change: Change | None = None

    @field_validator("data", mode="before")
    def validate_data(cls, value, values):
        type_map = {
            EventTypeEnum.TASK: Task,
            EventTypeEnum.MILESTONE: Milestone,
            EventTypeEnum.USERSTORY: UserStory,
            EventTypeEnum.EPIC: Epic,
            EventTypeEnum.WIKIPAGE: Wiki,
            EventTypeEnum.ISSUE: Issue,
        }

        target_type = type_map.get(values.data.get("type"))
        if not target_type:
            raise ValueError(f"Неизвестный тип: {values['type']}")

        if isinstance(value, dict):
            return target_type(**value)

        return value
