from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, RootModel, field_validator

from src.core.settings import get_settings
from src.entities.schemas.webhook_data.nested_schemas import FromTo


class DiffMilestone(FromTo):
    pass


class DiffSprintOrder(FromTo):
    pass


class DiffDueDate(FromTo):
    pass


class DiffStatus(FromTo):
    pass


class DiffBlockedNote(FromTo):
    pass


class DiffBlockedNoteHTML(FromTo):
    pass


class IsBlocked(FromTo):
    pass


class IsIocaine(FromTo):
    pass


class Tags(FromTo):
    pass


class AssignedTo(FromTo):
    pass


class AssignedUsers(FromTo):
    pass


class Name(FromTo):
    pass


class Subject(FromTo):
    pass


class EstimatedStart(FromTo):
    pass


class EstimatedFinish(FromTo):
    pass


class TeamRequirements(FromTo):
    pass


class ClientRequirements(FromTo):
    pass


class DiffTypePrioritySeverity(FromTo):
    pass


class Points(RootModel):
    root: dict[str, FromTo]


class DiffContent(FromTo):
    pass


class DiffContentHtml(FromTo):
    pass


class DiffBaseAttachment(BaseModel):
    filename: str | None = None
    url: str | None = None


class DiffAttachment(DiffBaseAttachment):
    id: int | None = None
    is_deprecated: bool | None = None
    description: str | list[str] | None = None


class DiffChanges(BaseModel):
    description: list[str] | None = None
    is_deprecated: list[bool] | None = None


class DiffChangeAttachment(DiffBaseAttachment):
    thumb_url: str | None = None
    changes: DiffChanges


class DiffAttachments(BaseModel):
    new: list[DiffAttachment] | None = None
    changed: list[DiffChangeAttachment] | None = None
    deleted: list[DiffAttachment] | None = None


class Diff(BaseModel):
    name: Name | None = None
    subject: Subject | None = None
    team_requirement: TeamRequirements | None = None
    client_requirement: ClientRequirements | None = None
    description_diff: str | None = None
    assigned_to: AssignedTo | None = None
    assigned_users: AssignedUsers | None = None
    is_blocked: IsBlocked | None = None
    is_iocaine: IsIocaine | None = None
    tags: Tags | None = None
    type: DiffTypePrioritySeverity | None = None
    priority: DiffTypePrioritySeverity | None = None
    severity: DiffTypePrioritySeverity | None = None
    blocked_note_diff: DiffBlockedNote | None = None
    blocked_note_html: DiffBlockedNoteHTML | None = None
    points: Points | None = None
    milestone: DiffMilestone | None = None
    sprint_order: DiffSprintOrder | None = None
    estimated_start: EstimatedStart | None = None
    estimated_finish: EstimatedFinish | None = None
    due_date: DiffDueDate | None = None
    status: DiffStatus | None = None
    attachments: DiffAttachments | None = None
    content_diff: DiffContent | None = None
    content_html: DiffContentHtml | None = None


class Change(BaseModel):
    comment: str | None = None
    comment_html: str | None = None
    edit_comment_date: datetime | None = None
    delete_comment_date: datetime | None = None
    diff: Diff | None = None

    @field_validator("edit_comment_date", mode="before")
    def edit_comment_date_to_local_tz(cls, value: str | datetime | None) -> datetime | None:
        if value is None:
            return None

        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        return value.astimezone(ZoneInfo(get_settings().TIME_ZONE))

    @field_validator("delete_comment_date", mode="before")
    def delete_comment_date_to_local_tz(cls, value: str | datetime | None) -> datetime | None:
        if value is None:
            return None

        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))

        return value.astimezone(ZoneInfo(get_settings().TIME_ZONE))
