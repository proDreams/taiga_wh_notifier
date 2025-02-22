from enum import Enum


class AdminActionTypeEnum(str, Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define various action types that can be performed in an editing context.
    :ivar menu: The menu object.
    :type menu: str
    :ivar add: The action type for add admin.
    :type add: str
    :ivar select: The action type for select admin.
    :type select: str
    :ivar remove: The action type for remove project.
    :type remove: str
    """

    menu = "menu"
    add = "add"
    select = "sel"
    remove = "rm"
