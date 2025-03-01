from enum import Enum


class CommandsEnum(str, Enum):
    """
    Enum for storing different command identifiers used in bot.

    :ivar START: Command identifier for initiating an action.
    :type START: str
    :ivar MENU: Command identifier for navigating to a menu option.
    :type MENU: str
    """

    START = "start"
    MENU = "menu"


class PaginationButtonsEnum(str, Enum):
    """
    Enum representing different types of buttons in a user interface.

    :ivar NO_BACK: Indicates that the back button should not work.
    :type NO_BACK: str
    :ivar NO_NEXT: Indicates that the next button should not work.
    :type NO_NEXT: str
    :ivar JUST_INFO: Indicates that only information buttons should work.
    :type JUST_INFO: str
    :ivar BLANK: Indicates that no pagination buttons should work.
    :type BLANK: str
    """

    NO_BACK = "no_back"
    NO_NEXT = "no_next"
    JUST_INFO = "just_info"
    BLANK = "blank"
