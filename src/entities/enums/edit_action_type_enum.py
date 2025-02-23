from enum import Enum


class BaseProjectMenuEnum(str, Enum):
    """
    This enumeration is used to define menu that can be performed in an editing context.
    :ivar MENU: The menu object.
    :type MENU: str
    """

    MENU = "menu"


class ProjectsCommonMenuEnum(str, Enum):
    """
    An enumeration representing different types of edit actions.

    This enumeration is used to define types that can be performed in an editing context.

    """

    ADD = "add"
    EDIT = "ed"


class ProjectSelectedMenuEnum(str, Enum):
    """
    Class representing the selection menu options for a project.

    This class provides an enumeration of string constants that represent different
    menu options available for selecting actions related to a project.

    :ivar EDIT_NAME: Enumeration value indicating the option to edit a project's name.
    :type EDIT_NAME: str

    :ivar REMOVE: Enumeration value indicating the option to remove a project.
    :type REMOVE: str
    """

    EDIT_NAME = "ed_n"
    EDIT_INSTANCE = "inst"
    REMOVE = "rm"


class ProjectInstanceActionEnum(str, Enum):
    """
    Enumerate for project instance actions.

    :ivar ADD: Action to add a project instance.
    :type ADD: str

    :ivar EDIT: Action to edit an existing project instance.
    :type EDIT: str
    """

    ADD = "add"
    EDIT = "ed"


class ProjectSelectedInstanceActionEnum(str, Enum):
    """
    Enumeration class for project selected instance actions.

    :ivar EDIT_FOLLOWING_ACTION_TYPE: Type of action to edit the following.
    :type EDIT_FOLLOWING_ACTION_TYPE: str

    :ivar EDIT_TARGET_PATH: Path to the target location to edit.
    :type EDIT_TARGET_PATH: str

    :ivar REMOVE: Action to remove a project instance.
    :type REMOVE: str
    """

    EDIT_FOLLOWING_ACTION_TYPE = "fat"
    EDIT_TARGET_PATH = "tr_pth"
    REMOVE = "rm"


class ProjectSelectedTargetPathEnum(str, Enum):
    """
    :ivar EDIT_CHAT_ID: The action type for edit project chat id.
    :type EDIT_CHAT_ID: str

    :ivar EDIT_THREAD_ID: The action type for edit project thread id.
    :type EDIT_THREAD_ID: str
    """

    EDIT_CHAT_ID = "ch_id"
    EDIT_THREAD_ID = "thr_id"


class ProjectSelectedTargetPathActionEnum(str, Enum):
    """
    An enumeration representing possible actions for event target paths.

    :ivar CHANGE: The action to change something.
    :type CHANGE: str

    :ivar REMOVE: The action to remove something.
    :type REMOVE: str
    """

    CHANGE = "ch"
    REMOVE = "rm"
