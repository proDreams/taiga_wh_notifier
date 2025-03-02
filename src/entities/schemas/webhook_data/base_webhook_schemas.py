from datetime import date, datetime

from pydantic import BaseModel, Field


class BaseID(BaseModel):
    id: int


class BasePermalink(BaseModel):
    permalink: str


class BaseName(BaseModel):
    name: str


class TimeStamped(BaseModel):
    created_date: datetime | None = None
    modified_date: datetime | None = None


class DiffMilestone(BaseModel):
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None


class DiffSprintOrder(BaseModel):
    from_: int | None = Field(default=None, alias="from")
    to: int | None = None


class DiffDueDate(BaseModel):
    from_: date | None = Field(default=None, alias="from")
    to: date | None = None


class DiffStatus(BaseModel):
    from_: str | None = Field(default=None, alias="from")
    to: str | None = None


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


class Diff(BaseModel):
    milestone: DiffMilestone | None = None
    sprint_order: DiffSprintOrder | None = None
    due_date: DiffDueDate | None = None
    status: DiffStatus | None = None
    attachments: DiffAttachments | None = None


class Change(BaseModel):
    comment: str | None
    # TODO: уточнить какой формат у `edit_comment_date`
    edit_comment_date: datetime | None = None
    delete_comment_date: datetime | None = None
    diff: Diff | None = None
