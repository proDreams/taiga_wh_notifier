from enum import Enum


class EventTypeEnum(str, Enum):
    epic = "epic"
    milestone = "milestone"
    userstory = "userstory"
    task = "task"
    issue = "issue"
    wikipage = "wikipage"
    test = "test"


class EventActionEnum(str, Enum):
    create = "create"
    delete = "delete"
    change = "change"
    test = "test"
