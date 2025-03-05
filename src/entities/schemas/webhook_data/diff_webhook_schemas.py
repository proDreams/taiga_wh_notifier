from datetime import datetime

from pydantic import BaseModel, RootModel

from src.entities.schemas.webhook_data.base_webhook_schemas import DiffAttachments
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


class AssignedTo(FromTo):
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


class Diff(BaseModel):
    name: Name | None = None
    subject: Subject | None = None
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
