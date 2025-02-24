from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.profile_callbacks import (
    ProfileActions,
    ProfileMenu,
    SelectChangeLanguage,
    SelectLanguageConfirm,
)
from src.entities.enums.profile_action_type_enum import (
    ProfileActionTypeEnum,
    ProfileMenuEnum,
)
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.logic.bot_logic.keyboards.dynamic_profile_keyboards import (
    create_allowed_lang_dict,
)
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.state_utils import get_info_for_state
from src.utils.text_utils import localize_text_to_message

profile_router = Router()

logger = Configuration.logger.get_logger(name=__name__)


@profile_router.callback_query(
    ProfileMenu.filter(ProfileMenuEnum.MENU == F.profile_menu), StateFilter(SingleState.active)
)
async def profile_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the profile menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param state: The state that triggered the callback query.
    :type state: FSMContext

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
        reply_markup=keyboard.create_static_keyboard(
            key="profile_menu_keyboard",
            lang=user.language_code,
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@profile_router.callback_query(
    ProfileActions.filter(ProfileActionTypeEnum.CHANGE_LANGUAGE == F.action_type), StateFilter(SingleState.active)
)
async def change_language_handler(
    callback: CallbackQuery,
    callback_data: ProfileActions,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The state that triggered the callback query.
    :type state: FSMContext

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
            buttons_dict=create_allowed_lang_dict(),
            lang=user.language_code,
            keyboard_type="inline",
            key_header_title="allowed_lang",
            key_in_storage="allowd_lang_dict",
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@profile_router.callback_query(
    SelectChangeLanguage.filter(ProfileActionTypeEnum.SELECT_LANGUAGE == F.action_type),
    StateFilter(SingleState.active),
)
async def select_change_language_handler(
    callback: CallbackQuery,
    callback_data: SelectChangeLanguage,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The state that triggered the callback query.
    :type state: FSMContext

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
            placeholder={
                "select_language": callback_data.select_language.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@profile_router.callback_query(SelectLanguageConfirm.filter(), StateFilter(SingleState.active))
async def confirm_select_change_language_handler(
    callback: CallbackQuery,
    callback_data: SelectLanguageConfirm,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The state that triggered the callback query.
    :type state: FSMContext

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
        reply_markup=keyboard.create_static_keyboard(
            key="select_change_lang_confirm",
            lang=user.language_code,
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@profile_router.callback_query()
async def catch_handl(callback_query: CallbackQuery) -> None:
    print(callback_query.data)
