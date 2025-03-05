from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from src.entities.schemas.webhook_data.base_webhook_schemas import (
    BaseID,
    BaseName,
    BasePermalink,
    BaseRequirement,
    TimeStamped,
)


class BaseEntity(BaseID, BasePermalink):
    """
    Nested:
     - id from BaseID;
     - permalink from BasePermalink;
    """

    pass


class User(BaseEntity):
    """
    Nested:
     - id from BaseEntity;
     - permalink from BaseEntity;
    """

    username: str
    full_name: str
    photo: str | None = None
    gravatar_id: str


class Project(BaseEntity):
    """
    Nested:
     - id from BaseEntity;
     - permalink from BaseEntity;
    """

    name: str
    logo_big_url: str | None = None


class Status(BaseID, BaseName):
    """
    Nested:
     - id from BaseID;
     - name from BaseName;
    """

    slug: str
    color: str
    is_closed: bool | None = None
    is_archived: bool | None = None


class Milestone(BaseEntity, TimeStamped, BaseName):
    """
    Nested:
     - id from BaseEntity;
     - permalink from BaseEntity;
     - created_date from TimeStamped;
     - name from BaseName;
    """

    slug: str
    estimated_start: date
    estimated_finish: date
    closed: bool
    disponibility: float
    project: Project
    owner: User


class TypePrioritySeverity(BaseID, BaseName):
    color: str | None = None


class BaseItem(BaseEntity, TimeStamped):
    """
    Nested:
     - id from BaseEntity;
     - permalink from BaseEntity;
     - created_date from TimeStamped;
     - modified_date from TimeStamped;
     - name from BaseName;
    """

    custom_attributes_values: dict[str, Any] | None = None
    ref: int | None = None
    due_date: datetime | None = None
    due_date_reason: str | None = None
    subject: str | None = None
    watchers: list[Any] = []
    is_blocked: bool | None = None
    blocked_note: str | None = None
    description: str | None = None
    tags: list[Any] = []
    project: Project
    owner: User
    assigned_to: User | None = None
    status: Status | None = None
    milestone: Milestone | None = None


class Point(BaseName):
    """
    Nested:
     - name from BaseName;
    """

    role: str
    value: float | None


class FromTo(BaseModel):
    from_: str | int | date | bool | None = Field(default=None, alias="from")
    to: str | int | date | bool | None


class UserStory(BaseItem):
    """
    Nested from BaseItem:
        - id
        - permalink
        - created_date
        - modified_date
        - name
        - custom_attributes_values
        - ref
        - due_date
        - due_date_reason
        - subject
        - watchers
        - is_blocked
        - blocked_note
        - description
        - tags
        - project
        - owner
        - assigned_to
        - status
        - milestone
    """

    is_closed: bool | None = None
    finish_date: datetime | None = None
    client_requirement: bool
    team_requirement: bool
    generated_from_issue: Any | None = None
    generated_from_task: Any | None = None
    from_task_ref: Any | None = None
    external_reference: Any | None = None
    tribe_gig: Any | None = None
    assigned_users: list[int] | None = None
    points: list[Point] = []


class Task(BaseItem):
    """
    Nested from BaseItem:
        - id
        - permalink
        - created_date
        - modified_date
        - name
        - custom_attributes_values
        - ref
        - due_date
        - due_date_reason
        - subject
        - watchers
        - is_blocked
        - blocked_note
        - description
        - tags
        - project
        - owner
        - assigned_to
        - status
        - milestone
    """

    finished_date: datetime | None
    us_order: int | None = None
    taskboard_order: int | None = None
    is_iocaine: bool | None = None
    external_reference: Any | None = None
    user_story: UserStory | None = None
    assigned_users: list[int] | None = None
    promoted_to: list[Any] = []


class Epic(BaseItem, BaseRequirement):
    pass


class Wiki(BaseEntity, TimeStamped):
    slug: str | None = None
    content: str | None = None
    project: Project | None = None


class Issue(BaseItem):
    external_reference: str | None = None
    type: TypePrioritySeverity | None = None
    priority: TypePrioritySeverity | None = None
    severity: TypePrioritySeverity | None = None
