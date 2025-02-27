from enum import Enum


class EventTypeEnum(str, Enum):
    """
    Enumeration of event types.

    :ivar EPIC: Represents an epic event.
    :type EPIC: str
    :ivar MILESTONE: Represents a milestone event.
    :type MILESTONE: str
    :ivar USERSTORY: Represents a user story event.
    :type USERSTORY: str
    :ivar TASK: Represents a task event.
    :type TASK: str
    :ivar ISSUE: Represents an issue event.
    :type ISSUE: str
    :ivar WIKIPAGE: Represents a wiki page event.
    :type WIKIPAGE: str
    :ivar TEST: Represents a test event.
    :type TEST: str
    """

    EPIC = "epic"
    MILESTONE = "milestone"
    USERSTORY = "userstory"
    TASK = "task"
    ISSUE = "issue"
    WIKIPAGE = "wikipage"
    TEST = "test"


class EventActionEnum(str, Enum):
    """
    Enumeration representing different actions that can be performed on events.

    :ivar CREATE: Represents the creation of an event.
    :type CREATE: str
    :ivar DELETE: Represents the deletion of an event.
    :type DELETE: str
    :ivar CHANGE: Represents a change in an existing event.
    :type CHANGE: str
    :ivar TEST: Represents a test or simulation of an event action.
    :type TEST: str
    """

    CREATE = "create"
    DELETE = "delete"
    CHANGE = "change"
    TEST = "test"
