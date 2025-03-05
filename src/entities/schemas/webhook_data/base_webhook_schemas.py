from datetime import datetime

from pydantic import BaseModel


class BaseID(BaseModel):
    id: int


class BasePermalink(BaseModel):
    permalink: str


class BaseName(BaseModel):
    name: str


class TimeStamped(BaseModel):
    created_date: datetime | None = None
    modified_date: datetime | None = None


class DiffAttachment(BaseModel):
    id: int | None = None
    filename: str | None = None
    url: str | None = None
    is_deprecated: bool | None = None
    description: str | list[str, str] | None = None


class DiffAttachments(BaseModel):
    new: list[DiffAttachment] | None = None
    changed: list[DiffAttachment] | None = None
    deleted: list[DiffAttachment] | None = None


class BaseRequirement(BaseModel):
    client_requirement: bool | None = None
    team_requirement: bool | None = None
