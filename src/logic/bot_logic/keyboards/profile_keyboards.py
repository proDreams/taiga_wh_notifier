from src.core.settings import Configuration
from src.entities.callback_classes.profile_callbacks import (
    ProfileMenu,
    SelectChangeLanguage,
)
from src.entities.enums.profile_action_type_enum import ProfileActionTypeEnum

logger = Configuration.logger.get_logger(name=__name__)


def create_profile_change_lang_dict(callback_data: ProfileMenu) -> dict:
    """
    Creates a dictionary for changing profile language based on allowed languages.

    :param callback_data: The current state of the profile menu.
    :type callback_data: ProfileMenu
    :returns: A dictionary representing the inline keyboard with available language options.
    :rtype: dict
    """
    allowed_languages = Configuration.settings.ALLOWED_LANGUAGES

    logger.info(f"allowed_languages: {allowed_languages}")
    result = {
        "keyboard_type": "inline",
        "row_width": [1, 1, 1, 1, 1],
        "fixed_top": [
            {"text": " ", "type": "callback", "data": "noop"},
            {"text": "Profile menu", "type": "callback", "data": "noop"},
            # тут будет вызов метода, который будет по action_type брать название меню
            {"text": " ", "type": "callback", "data": "noop"},
        ],
        "button": [],
        "fixed_bottom": [
            {"text": "Back to menu", "type": "callback", "data": "{previous_callback}"},
            {"text": " ", "type": "callback", "data": "noop"},
        ],
    }
    for lang_code in allowed_languages:
        text = lang_code
        logger.info(f"callback_data: {callback_data}")
        callback_str = SelectChangeLanguage(
            action_type=ProfileActionTypeEnum.SELECT_LANGUAGE, select_language=lang_code
        ).pack()

        result["button"].append({"text": text, "type": "callback", "data": callback_str})
    return result
