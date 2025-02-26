from enum import Enum


class CommandsEnum(str, Enum):
    START = "start"
    MENU = "menu"


class PaginationButtonsEnum(str, Enum):
    NO_BACK = "no_back"
    NO_NEXT = "no_next"
    JUST_INFO = "just_info"
    BLANK = "blank"
