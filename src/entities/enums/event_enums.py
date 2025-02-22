from enum import Enum


class EventTypeEnum(str, Enum):
    EPIC = "epic"
    MILESTONE = "milestone"
    USERSTORY = "userstory"
    TASK = "task"
    ISSUE = "issue"
    WIKIPAGE = "wikipage"
    TEST = "test"


class EventActionEnum(str, Enum):
    CREATE = "create"
    DELETE = "delete"
    CHANGE = "change"
    TEST = "test"
