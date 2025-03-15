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

    :ivar ASSIGNED_TO: Changes related to the assignment of responsible persons.
    :type ASSIGNED_TO: str
    :ivar ASSIGNED_USERS: Changes related to the assignment of responsible persons (for userstory object).
    :type ASSIGNED_USERS: str
    :ivar ATTACHMENTS: Changes related to actions with attachments.
    :type ATTACHMENTS: str
    :ivar CLIENT_REQUIREMENT: Changes to the "Client Requirement" label.
    :type CLIENT_REQUIREMENT: str
    :ivar CONTENT_HTML: Changes related to actions with the Wiki content.
    :type CONTENT_HTML: str
    :ivar DESCRIPTION: Changes related to actions with the description field.
    :type DESCRIPTION: str
    :ivar DUE_DATE: Changes related to the due date.
    :type DUE_DATE: str
    :ivar ESTIMATED_FINISH: Changes related to the sprint finish date.
    :type ESTIMATED_FINISH: str
    :ivar ESTIMATED_START: Changes related to the sprint start date.
    :type ESTIMATED_START: str
    :ivar IS_BLOCKED: Changes related to the "is_blocked" label.
    :type IS_BLOCKED: str
    :ivar IS_IOCAINE: Changes related to the "is_iocaine" label.
    :type IS_IOCAINE: str
    :ivar MILESTONE: Changes related to sprint binding.
    :type MILESTONE: str
    :ivar NAME: Changes related to the object name.
    :type NAME: str
    :ivar POINTS: Changes related to points.
    :type POINTS: str
    :ivar PRIORITY: Changes to the "Priority" field of the "Task" object.
    :type PRIORITY: str
    :ivar SEVERITY: Changes to the "Severity" field of the "Task" object.
    :type SEVERITY: str
    :ivar STATUS: Changes to the "Status" field of the object.
    :type STATUS: str
    :ivar SUBJECT: Changes related to the object name.
    :type SUBJECT: str
    :ivar TEAM_REQUIREMENT: Changes to the "Team Requirement" label.
    :type TEAM_REQUIREMENT: str
    :ivar TAGS: Changes related to the object tags.
    :type TAGS: str
    :ivar TYPE: Changes to the "Type" field of the "Task" object.
    :type TYPE: str
    """

    ASSIGNED_TO = "assigned_to"
    ASSIGNED_USERS = "assigned_users"
    ATTACHMENTS = "attachments"
    CLIENT_REQUIREMENT = "client_requirement"
    CONTENT_HTML = "content_html"
    DESCRIPTION = "description"
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
    TAGS = "tags"
    TYPE = "type"


class EventParentsEnum(str, Enum):
    """
    Enumeration of event types that can be parents for other types.

    :ivar PROJECT: Represents a project event.
    :type PROJECT: str
    :ivar EPIC: Represents an epic event.
    :type EPIC: str
    :ivar MILESTONE: Represents a milestone event.
    :type MILESTONE: str
    :ivar USERSTORY: Represents a user story event.
    :type USERSTORY: str
    """

    PROJECT = "project"
    EPIC = "epic"
    MILESTONE = "milestone"
    USERSTORY = "userstory"


class EventFieldsEnum(str, Enum):
    """
    Enumeration for fields used in a message template.

    :ivar ACTION: Field containing information about the action.
    :type ACTION: str
    :ivar ASSIGNED_TO: Field containing information about the assignment of responsible persons.
    :type ASSIGNED_TO: str
    :ivar BY_FULLNAME: Field containing information about the full name of the action author.
    :type BY_FULLNAME: str
    :ivar CHANGE: Field containing information about the change actions.
    :type CHANGE: str
    :ivar CLIENT_REQUIREMENT: Field containing information about the "Client Requirement" label.
    :type CLIENT_REQUIREMENT: str
    :ivar DESCRIPTION: Field containing description information.
    :type DESCRIPTION: str
    :ivar DUE_DATE: Field containing information about the due date.
    :type DUE_DATE: str
    :ivar ESTIMATED_FINISH: Field containing information about the sprint finish date.
    :type ESTIMATED_FINISH: str
    :ivar IS_BLOCKED: Field containing information about the "is_blocked" label.
    :type IS_BLOCKED: str
    :ivar IS_IOCAINE: Field containing information about the "is_iocaine" label.
    :type IS_IOCAINE: str
    :ivar OBJECT_OF_ACTION: Field containing information about the type, name, and permalink of the object.
    :type OBJECT_OF_ACTION: str
    :ivar PARENTS: Field containing information about the parents of the objects.
    :type PARENTS: str
    :ivar POINTS: Field containing information about the points.
    :type POINTS: str
    :ivar PRIORITY: Field containing information about the task's "Priority".
    :type PRIORITY: str
    :ivar SEVERITY: Field containing information about the task's "Severity".
    :type SEVERITY: str
    :ivar STATUS: Field containing information about the object status.
    :type STATUS: str
    :ivar TAGS: Field containing information about the object tags.
    :type TAGS: str
    :ivar TEAM_REQUIREMENT: Field containing information about the "Team Requirement" label.
    :type TEAM_REQUIREMENT: str
    :ivar TIMESTAMP: Field containing information about the date and time of the action.
    :type TIMESTAMP: str
    :ivar TYPE: Field containing information about the task's "Type".
    :type TYPE: str
    """

    ACTION = "action"
    ASSIGNED_TO = "assigned_to"
    BY_FULLNAME = "by_fullname"
    CHANGE = "change"
    CLIENT_REQUIREMENT = "client_requirement"
    DESCRIPTION = "description"
    DUE_DATE = "due_date"
    ESTIMATED_FINISH = "estimated_finish"
    IS_BLOCKED = "is_blocked"
    IS_IOCAINE = "is_iocaine"
    OBJECT_OF_ACTION = "object_of_action"
    PARENTS = "parents"
    POINTS = "points"
    PRIORITY = "priority"
    SEVERITY = "severity"
    STATUS = "status"
    TAGS = "tags"
    TEAM_REQUIREMENT = "team_requirement"
    TIMESTAMP = "timestamp"
    TYPE = "type"


class EventObjectNameField(str, Enum):
    """
    Enumeration for fields used in a message template.

    :ivar NAME: Field containing name string for Milestone object.
    :type NAME: str
    :ivar SUBJECT: Field containing name string for Epic, Userstory, Task, Issue object.
    :type SUBJECT: str
    """

    NAME = "name"
    SUBJECT = "subject"


class EventAttachmentsChangesField(str, Enum):
    """
    Enumeration for fields used in a message template.

    :ivar DESCRIPTION: Field containing info about changes of the file description.
    :type DESCRIPTION: str
    :ivar IS_DEPRECATED: Field containing info about changes of the "IS_DEPRECATED" label.
    :type IS_DEPRECATED: str
    """

    DESCRIPTION = "description"
    IS_DEPRECATED = "is_deprecated"
