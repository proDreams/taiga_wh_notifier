from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.ProfileMenu import (
    ProfileMenu,
    SelectChangeLanguage,
    SelectLanguageConfirm,
)
from src.entities.enums.profile_action_type_enum import ProfileActionTypeEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.logic.bot_logic.keyboards.profile_keyboards import (
    create_profile_change_lang_dict,
)
from src.utils.text_utils import format_text_with_kwargs

profile_router = Router()

logger = Configuration.logger.get_logger(name=__name__)


@profile_router.callback_query(ProfileMenu.filter(ProfileActionTypeEnum.menu == F.action_type))
async def profile_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the profile menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_profile"),
        reply_markup=keyboard.create_static_keyboard(key="profile_menu_keyboard", lang="ru"),
    )


@profile_router.callback_query(ProfileMenu.filter(ProfileActionTypeEnum.change_language == F.action_type))
async def change_language_handler(
    callback: CallbackQuery,
    callback_data: ProfileMenu,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the change language menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    result_message = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_change_language"),
        user_lang=user.language_code,
    )

    await callback.message.edit_text(
        text=result_message,
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=create_profile_change_lang_dict(callback_data=callback_data),
            lang=user.language_code,
            key_in_storage="create_profile_change_lang_dict",
        ),
    )


@profile_router.callback_query(SelectChangeLanguage.filter(ProfileActionTypeEnum.select_language == F.action_type))
async def select_change_language_handler(
    callback: CallbackQuery,
    callback_data: SelectChangeLanguage,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the change language menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    result_message = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_select_change_language"),
        current_user_lang=user.language_code,
        new_user_lang=callback_data.select_language.value,
    )

    await callback.message.edit_text(
        text=result_message,
        reply_markup=keyboard.create_static_keyboard(
            key="select_change_lang",
            lang=callback_data.select_language.value,
            placeholder={"select_language": callback_data.select_language.value},
        ),
    )


@profile_router.callback_query(SelectLanguageConfirm.filter())
async def confirm_select_change_language_handler(
    callback: CallbackQuery,
    user: UserSchema,
    callback_data: SelectLanguageConfirm,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the change language menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param callback_data: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    """

    # TODO: здесь нужен обработчик установки языка

    result_message = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_confirm_select_change_language"),
        current_user_lang=user.language_code,
    )

    await callback.message.edit_text(
        result_message, reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="ru")
    )
