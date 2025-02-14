from datetime import date, datetime
from typing import Any

from src.entities.schemas.webhook_data.base_webhook_schemas import (
    BaseID,
    BaseName,
    BasePermalink,
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
    photo: str
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
    is_closed: bool
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
    estimated_start: date  # Формат "YYYY-MM-DD"
    estimated_finish: date
    closed: bool
    disponibility: float
    project: Project
    owner: User


class BaseItem(BaseEntity, TimeStamped):
    """
    Nested:
     - id from BaseEntity;
     - permalink from BaseEntity;
     - created_date from TimeStamped;
     - modified_date from TimeStamped;
     - name from BaseName;
    """

    custom_attributes_values: dict[str, Any]
    ref: int
    due_date: datetime | None
    due_date_reason: str
    subject: str
    watchers: list[Any] = []
    is_blocked: bool
    blocked_note: str
    description: str
    tags: list[Any] = []
    project: Project
    owner: User
    assigned_to: User | None
    status: Status
    milestone: Milestone


class Point(BaseName):
    """
    Nested:
     - name from BaseName;
    """

    role: str
    value: float | None


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

    is_closed: bool
    finish_date: datetime | None
    client_requirement: bool
    team_requirement: bool
    generated_from_issue: Any | None
    generated_from_task: Any | None
    from_task_ref: Any | None
    external_reference: Any | None
    tribe_gig: Any | None
    assigned_users: list[int]
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
    us_order: int
    taskboard_order: int
    is_iocaine: bool
    external_reference: Any | None
    user_story: UserStory
    promoted_to: list[Any] = []
