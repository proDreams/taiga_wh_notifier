from datetime import datetime

from pydantic import BaseModel

from src.entities.schemas.webhook_data.nested_schemas import (
    AssignedTo,
    ClientRequirements,
    DiffBlockedNote,
    DiffBlockedNoteHTML,
    DiffDueDate,
    DiffMilestone,
    DiffSprintOrder,
    DiffStatus,
    DiffTypePrioritySeverity,
    IsBlocked,
    IsIocaine,
    Name,
    Points,
    TeamRequirements,
)


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


class Diff(BaseModel):
    name: Name | None = None
    team_requirement: TeamRequirements | None = None
    client_requirement: ClientRequirements | None = None
    description_diff: str | None = None
    assigned_to: AssignedTo | None = None
    is_blocked: IsBlocked | None = None
    is_iocaine: IsIocaine | None = None
    type: DiffTypePrioritySeverity | None = None
    priority: DiffTypePrioritySeverity | None = None
    severity: DiffTypePrioritySeverity | None = None
    blocked_note_diff: DiffBlockedNote | None = None
    blocked_note_html: DiffBlockedNoteHTML | None = None
    points: Points | None = None
    milestone: DiffMilestone | None = None
    sprint_order: DiffSprintOrder | None = None
    due_date: DiffDueDate | None = None
    status: DiffStatus | None = None
    attachments: DiffAttachments | None = None


class Change(BaseModel):
    comment: str | None = None
    edit_comment_date: datetime | None = None
    delete_comment_date: datetime | None = None
    diff: Diff | None = None
