from enum import Enum


class AdminMenuEnum(str, Enum):
    """
    This enumeration is used to define menu action types that can be performed in an editing context.

    :ivar MENU: The menu object.
    :type MENU: str
    """

    MENU = "menu"


class AdminActionTypeEnum(str, Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define various action types that can be performed in an editing context.

    :ivar ADD: The action type for add admin.
    :type ADD: str
    :ivar SELECT: The action type for select admin.
    :type SELECT: str
    :ivar REMOVE: The action type for remove project.
    :type REMOVE: str
    """

    ADD = "add"
    SELECT = "sel"
    REMOVE = "rm"
