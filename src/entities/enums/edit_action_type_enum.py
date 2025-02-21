from enum import Enum


class EditActionTypeEnum(Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define various action types that can be performed in an editing context.
    :ivar menu: The menu object.
    :type menu: str
    :ivar edit_name: The action type for edit project name.
    :type edit_name: str
    :ivar remove: The action type for remove project.
    :type remove: str
    """

    menu = "menu"
    add = "add"
    edit = "ed"
    edit_name = "ed_n"
    edit_following_action_type = "fat"
    remove = "rm"


class EditTargetPathEnum(Enum):
    """
    :ivar edit_chat_id: The action type for edit project chat id.
    :type edit_chat_id: str
    :ivar edit_thread_id: The action type for edit project thread id.
    :type edit_thread_id: str
    """

    edit_chat_id = "ch_id"
    edit_thread_id = "thr_id"


class EventTargetPathActionEnum(Enum):
    add = "add"
    change = "ch"
    remove = "rm"
