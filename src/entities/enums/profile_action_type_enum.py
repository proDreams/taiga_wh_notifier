from enum import Enum


class ProfileMenuEnum(str, Enum):
    """
    Represents the different menu options in a user profile system.
    :ivar MENU: The action type for add admin.
    :type MENU: str
    """

    MENU = "menu"


class ProfileActionTypeEnum(str, Enum):
    """
    Represents the allowed menu options in a user profile system.
    :ivar CHANGE_LANGUAGE: The action type for step to change language.
    :type CHANGE_LANGUAGE: str
    :ivar SELECT_LANGUAGE: The action type for select and apply language.
    :type SELECT_LANGUAGE: str
    """

    CHANGE_LANGUAGE = "ch_lang"
    SELECT_LANGUAGE = "lang"
