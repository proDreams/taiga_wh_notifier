from datetime import datetime
from typing import Literal

from pydantic import BaseModel

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
    type: Literal["task", "milestone", "userstory", "epic", "wikipage", "issue"]
    by: User
    date: datetime
    data: Task | Milestone | UserStory | Epic | Wiki | Issue
    change: Change | None = None
