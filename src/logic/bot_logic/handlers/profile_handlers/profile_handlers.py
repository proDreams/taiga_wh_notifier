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
from src.utils.send_message_utils import send_message
from src.utils.text_utils import localize_text_to_message

profile_router = Router()

logger = Configuration.logger.get_logger(name=__name__)


@profile_router.callback_query(ProfileMenu.filter(ProfileActionTypeEnum.menu == F.action_type))
async def profile_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the profile menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    # TODO: сделать user_status в модель `user`
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_profile",
            lang=user.language_code,
            tg_user_id=str(user.telegram_id),
            is_admin="ВАНЯ СДЕЛАЕТ АДМИНА",
            user_lang=user.language_code,
        ),
        reply_markup=keyboard.create_static_keyboard(key="profile_menu_keyboard", lang=user.language_code),
        try_to_edit=True,
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

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_change_language", lang=user.language_code, user_lang=user.language_code
        ),
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=create_profile_change_lang_dict(callback_data=callback_data),
            lang=user.language_code,
            key_in_storage="create_profile_change_lang_dict",
        ),
        try_to_edit=True,
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

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_select_change_language",
            lang=user.language_code,
            current_user_lang=user.language_code,
            new_user_lang=callback_data.select_language.value,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="select_change_lang",
            lang=user.language_code,
            placeholder={"select_language": callback_data.select_language.value},
        ),
        try_to_edit=True,
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

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_confirm_select_change_language",
            lang=user.language_code,
            current_user_lang=user.language_code,
        ),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang=user.language_code),
        try_to_edit=True,
    )
