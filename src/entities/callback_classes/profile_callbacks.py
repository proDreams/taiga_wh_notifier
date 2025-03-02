from aiogram.filters.callback_data import CallbackData

from src.entities.enums.lang_enum import LanguageEnum


class ProfileMenuData(CallbackData, prefix="profile_menu"):
    pass


class ChangeLanguage(CallbackData, prefix="profile_change_language"):
    page: int = 0


class SelectChangeLanguage(CallbackData, prefix="profile_select_language"):
    select_language: LanguageEnum


class SelectChangeLanguageConfirmData(SelectChangeLanguage, prefix="select_change_language_confirm"):
    pass
