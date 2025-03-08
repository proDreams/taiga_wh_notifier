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


class EventChangeEnum(str, Enum):
    """
    Enumeration representing different actions that can be performed on change events.

    :ivar ASSIGNED_TO: Changes related to the assignment of responsible persons
    :type ASSIGNED_TO: str
    :ivar ATTACHMENTS: Changes related to actions with attachments
    :type ATTACHMENTS: str
    :ivar CLIENT_REQUIREMENT: Changes to the "Client Requirement" label
    :type CLIENT_REQUIREMENT: str
    :ivar CONTENT_HTML: Changes related to actions with the Wiki content
    :type CONTENT_HTML: str
    :ivar DESCTRIPTION: Changes related to actions with the description field
    :type DESCTRIPTION: str
    :ivar DUE_DATE: Changes related to the due date
    :type DUE_DATE: str
    :ivar ESTIMATED_FINISH: Changes related to the sprint finish date
    :type ESTIMATED_FINISH: str
    :ivar ESTIMATED_START: Changes related to the sprint start date
    :type ESTIMATED_START: str
    :ivar IS_BLOCKED: Changes related to the "is_blocking" label
    :type IS_BLOCKED: str
    :ivar IS_IOCAINE: Changes related to the "is_iocaine" label
    :type IS_IOCAINE: str
    :ivar MILESTONE: Changes related to sprint binding
    :type MILESTONE: str
    :ivar NAME: Changes related to the object name
    :type NAME: str
    :ivar POINTS: Changes related to points
    :type POINTS: str
    :ivar PRIORITY: Changes to the "Priority" field of the "Task" object
    :type PRIORITY: str
    :ivar SEVERITY: Changes to the "Severity" field of the "Task" object
    :type SEVERITY: str
    :ivar STATUS: Changes to the "Status" field of the object
    :type STATUS: str
    :ivar SUBJECT: Changes related to the object name
    :type SUBJECT: str
    :ivar TEAM_REQUIREMENT: Changes to the "Team Requirement" label
    :type TEAM_REQUIREMENT: str
    :ivar TYPE: Changes to the "Type" field of the "Task" object
    :type TYPE: str
    """

    ASSIGNED_TO = "assigned_to"
    ATTACHMENTS = "attachments"
    CLIENT_REQUIREMENT = "client_requirement"
    CONTENT_HTML = "content_html"
    DESCTRIPTION = "description"
    DUE_DATE = "due_date"
    ESTIMATED_FINISH = "estimated_finish"
    ESTIMATED_START = "estimated_start"
    IS_BLOCKED = "is_blocked"
    IS_IOCAINE = "is_iocaine"
    MILESTONE = "milestone"
    NAME = "name"
    POINTS = "points"
    PRIORITY = "priority"
    SEVERITY = "severity"
    STATUS = "status"
    SUBJECT = "subject"
    TEAM_REQUIREMENT = "team_requirement"
    TYPE = "type"
