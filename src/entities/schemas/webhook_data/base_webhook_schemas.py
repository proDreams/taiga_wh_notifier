from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, field_validator

from src.core.settings import get_settings


class BaseID(BaseModel):
    id: int


class BasePermalink(BaseModel):
    permalink: str


class BaseName(BaseModel):
    name: str


class TimeStamped(BaseModel):
    created_date: datetime | None = None
    modified_date: datetime | None = None

    @field_validator("created_date", mode="before")
    def created_date_to_local_tz(cls, value: str | datetime | None) -> datetime | None:
        if value is None:
            return None

        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        return value.astimezone(ZoneInfo(get_settings().TIME_ZONE))

    @field_validator("modified_date", mode="before")
    def modified_date_to_local_tz(cls, value: str | datetime | None) -> datetime | None:
        if value is None:
            return None

        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        return value.astimezone(ZoneInfo(get_settings().TIME_ZONE))


class BaseRequirement(BaseModel):
    client_requirement: bool | None = None
    team_requirement: bool | None = None
