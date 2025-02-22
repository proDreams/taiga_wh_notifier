from enum import Enum


class AdminActionTypeEnum(str, Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define various action types that can be performed in an editing context.
    :ivar MENU: The menu object.
    :type MENU: str
    :ivar ADD: The action type for add admin.
    :type ADD: str
    :ivar select: The action type for select admin.
    :type select: str
    :ivar REMOVE: The action type for remove project.
    :type REMOVE: str
    """

    MENU = "menu"
    ADD = "add"
    SELECT = "sel"
    REMOVE = "rm"
