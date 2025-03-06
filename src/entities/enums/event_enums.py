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

    :ivar ASSIGNED_TO: Изменения, связанные с назначением ответственных
    :type ASSIGNED_TO: str
    :ivar ATTACHMENTS: Изменения, связанные с действиями с вложениями
    :type ATTACHMENTS: str
    :ivar CLIENT_REQUIREMENT: Изменения метки "Требование клиента"
    :type CLIENT_REQUIREMENT: str
    :ivar CONTENT_HTML: Изменения, связанные с деqствиями c содержимым Wiki
    :type CONTENT_HTML: str
    :ivar DESCTRIPTION: Изменения, связанные с дествиями с полем описание
    :type DESCTRIPTION: str
    :ivar DUE_DATE: Изменения, связанные с датой дедлайна
    :type DUE_DATE: str
    :ivar ESTIMATED_FINISH: Изменения, связанные с датой окончания спринта
    :type ESTIMATED_FINISH: str
    :ivar ESTIMATED_START: Изменения, связанные с датой начала спринта
    :type ESTIMATED_START: str
    :ivar IS_BLOCKED: Изменения, связанные с блокировкой
    :type IS_BLOCKED: str
    :ivar IS_IOCAINE: Изменения, связанные с меткой Йокаин
    :type IS_IOCAINE: str
    :ivar MILESTONE: Изменения, связанные с привязкой к спринту
    :type MILESTONE: str
    :ivar POINTS: Изменения, связанные очками
    :type POINTS: str
    :ivar PRIORITY: Изменения поля "Приоритет" объекта "Задача"
    :type PRIORITY: str
    :ivar SEVERITY: Изменения поля "Важность" объекта "Задача"
    :type SEVERITY: str
    :ivar STATUS: Изменения поля "Статус" объекта
    :type STATUS: str
    :ivar SUBJECT: Изменения, связанные с именем объекта
    :type SUBJECT: str
    :ivar TEAM_REQUIREMENT: Изменения метки "Требование команды"
    :type TEAM_REQUIREMENT: str
    :ivar TYPE: Изменения поля "Тип" объекта
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
