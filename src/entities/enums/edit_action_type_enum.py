from enum import Enum


class EditActionTypeEnum(str, Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define various action types that can be performed in an editing context.
    :ivar MENU: The menu object.
    :type MENU: str
    :ivar EDIT_NAME: The action type for edit project name.
    :type EDIT_NAME: str
    :ivar REMOVE: The action type for remove project.
    :type REMOVE: str
    """

    MENU = "menu"
    ADD = "add"
    EDIT = "ed"
    EDIT_NAME = "ed_n"
    EDIT_FOLLOWING_ACTION_TYPE = "fat"
    REMOVE = "rm"


class EditTargetPathEnum(str, Enum):
    """
    :ivar EDIT_CHAT_ID: The action type for edit project chat id.
    :type EDIT_CHAT_ID: str
    :ivar EDIT_THREAD_ID: The action type for edit project thread id.
    :type EDIT_THREAD_ID: str
    """

    EDIT_CHAT_ID = "ch_id"
    EDIT_THREAD_ID = "thr_id"


class EventTargetPathActionEnum(str, Enum):
    ADD = "add"
    CHANGE = "ch"
    REMOVE = "rm"
