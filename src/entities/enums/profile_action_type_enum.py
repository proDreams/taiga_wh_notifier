from enum import Enum


class ProfileActionTypeEnum(str, Enum):
    MENU = "menu"
    CHANGE_LANGUAGE = "ch_lang"
    SELECT_LANGUAGE = "lang"
