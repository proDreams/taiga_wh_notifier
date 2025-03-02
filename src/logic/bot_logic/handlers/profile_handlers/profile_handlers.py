from aiogram import Router
from aiogram.types import CallbackQuery

from src.core.settings import get_logger
from src.entities.callback_classes.profile_callbacks import (
    ChangeLanguage,
    ProfileMenuData,
    SelectChangeLanguage,
    SelectChangeLanguageConfirmData,
)
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.logic.services.profile_service import ProfileService
from src.logic.services.user_service import UserService
from src.utils.send_message_utils import send_message
from src.utils.text_utils import localize_text_to_message

profile_router = Router()

logger = get_logger(name=__name__)


@profile_router.callback_query(ProfileMenuData.filter())
async def profile_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the profile menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    # TODO: сделать user_status в модель `user`
    kb_key = "profile_menu_keyboard"
    message_key = "message_to_profile"

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
        is_admin=user.is_admin,
        tg_user_id=str(user.telegram_id),
        user_lang=user.language_code,
    )

    keyboard = await keyboard_generator.generate_static_keyboard(kb_key=kb_key, lang=user.language_code)

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@profile_router.callback_query(ChangeLanguage.filter())
async def change_language_handler(
    callback: CallbackQuery,
    callback_data: ChangeLanguage,
    user: UserSchema,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the change language menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback: ChangeLanguage

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    page = callback_data.page
    data, count = await ProfileService().get_languages(page=page)
    text = localize_text_to_message(
        text_in_yaml="message_to_change_language", lang=user.language_code, user_lang=user.language_code
    )

    keyboard = await keyboard_generator.generate_dynamic_keyboard(
        kb_key="change_language_menu", data=data, lang=user.language_code, count=count, page=page
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@profile_router.callback_query(SelectChangeLanguage.filter())
async def select_change_language_handler(
    callback: CallbackQuery,
    callback_data: SelectChangeLanguage,
    user: UserSchema,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the change language menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback: SelectChangeLanguage

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """

    kb_key = "select_change_lang_keyboard"
    message_key = "message_to_select_change_language"

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
        current_user_lang=user.language_code,
        new_user_lang=callback_data.select_language.value,
    )

    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key=kb_key, lang=user.language_code, select_language=callback_data.select_language
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@profile_router.callback_query(SelectChangeLanguageConfirmData.filter())
async def confirm_select_change_language_handler(
    callback: CallbackQuery,
    callback_data: SelectChangeLanguageConfirmData,
    user: UserSchema,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the change language menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback: SelectChangeLanguageConfirmData

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    """
    language = callback_data.select_language
    await UserService().update_user(user_id=user.id, field="language_code", value=language)
    kb_key = "select_change_lang_confirm_keyboard"
    message_key = "message_to_confirm_select_change_language"

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
        current_user_lang=user.language_code,
    )

    keyboard = await keyboard_generator.generate_static_keyboard(kb_key=kb_key, lang=user.language_code)

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@profile_router.callback_query()
async def catch_handl(callback_query: CallbackQuery) -> None:
    print(callback_query.data)
