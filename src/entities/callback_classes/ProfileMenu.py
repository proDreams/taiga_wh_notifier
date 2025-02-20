from aiogram.filters.callback_data import CallbackData

from src.entities.enums.lang_enum import LanguageEnum
from src.entities.enums.profile_action_type_enum import ProfileActionTypeEnum


class ProfileMenu(CallbackData, prefix="profile"):
    action_type: ProfileActionTypeEnum


class SelectChangeLanguage(ProfileMenu, prefix="profile"):
    select_language: LanguageEnum


class SelectLanguageConfirm(SelectChangeLanguage, prefix="profile"):
    confirm_language: str = "true"
