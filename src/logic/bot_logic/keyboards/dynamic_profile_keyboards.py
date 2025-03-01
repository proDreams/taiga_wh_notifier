from src.core.settings import get_logger, get_settings
from src.entities.callback_classes.profile_callbacks import SelectChangeLanguage
from src.entities.enums.profile_action_type_enum import ProfileActionTypeEnum
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator

logger = get_logger(name=__name__)


def create_allowed_lang_dict() -> dict:
    """
    Creates a dictionary containing allowed admin buttons for language selection.

    :return: A dictionary representing the dynamic data for keyboard generation with allowed language buttons.
    :rtype: dict

    """
    allowed_languages = get_settings().ALLOWED_LANGUAGES

    result_allowed_lang_buttons = []
    for lang_code in allowed_languages:
        text = lang_code
        callback_str = SelectChangeLanguage(
            action_type=ProfileActionTypeEnum.SELECT_LANGUAGE,
            select_language=lang_code,
        ).pack()

        result_allowed_lang_buttons.append({"text": text, "type": "callback", "data": callback_str})

    return KeyboardGenerator.get_dynamic_data(result_allowed_lang_buttons)
