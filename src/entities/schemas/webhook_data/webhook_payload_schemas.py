from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from src.entities.schemas.webhook_data.base_webhook_schemas import Change
from src.entities.schemas.webhook_data.nested_schemas import (
    Milestone,
    Task,
    User,
    UserStory,
)


class WebhookPayload(BaseModel):
    action: str
    type: Literal["task", "milestone", "userstory"]
    by: User
    date: datetime
    data: Task | Milestone | UserStory
    change: Change | None = None
