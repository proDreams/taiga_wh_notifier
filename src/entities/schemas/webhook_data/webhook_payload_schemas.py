from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, field_validator

from src.core.settings import get_settings
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.webhook_data.diff_webhook_schemas import Change
from src.entities.schemas.webhook_data.nested_schemas import (
    Epic,
    Issue,
    Milestone,
    Task,
    Test,
    User,
    UserStory,
    Wiki,
)


class WebhookPayload(BaseModel):
    action: str
    type: EventTypeEnum
    by: User
    date: datetime
    data: Task | Milestone | UserStory | Epic | Wiki | Issue | Test
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
            EventTypeEnum.TEST: Test,
        }

        target_type = type_map.get(values.data.get("type"))
        if not target_type:
            raise ValueError(f"Неизвестный тип: {values['type']}")

        if isinstance(value, dict):
            return target_type(**value)

        return value

    @field_validator("date", mode="before")
    def convert_to_local_tz(cls, value: str | datetime | None) -> datetime | None:
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        return value.astimezone(ZoneInfo(get_settings().TIME_ZONE))
