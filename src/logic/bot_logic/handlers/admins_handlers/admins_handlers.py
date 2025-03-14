from random import randint

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import get_logger
from src.entities.callback_classes.admin_callbacks import (
    AdminAddData,
    AdminManageData,
    AdminMenuData,
    AdminRemoveConfirmData,
    AdminRemoveData,
)
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.admin_states import ShareUsersSteps
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.logic.services.user_service import UserService
from src.utils.send_message_utils import send_message
from src.utils.text_utils import localize_text_to_message

admin_router = Router()

logger = get_logger(name=__name__)


@admin_router.callback_query(AdminMenuData.filter())
async def admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard_generator: KeyboardGenerator, callback_data: AdminMenuData
) -> None:
    """
    Handles callback queries for the admin menu.

    :param callback: Callback query received from the user.
    :type callback: CallbackQuery
    :param user: User schema containing user information.
    :type user: UserSchema
    :param keyboard_generator: Generator responsible for creating dynamic keyboards.
    :type keyboard_generator: KeyboardGenerator
    :param callback_data: Data associated with the admin menu callback query.
    :type callback_data: AdminMenuData
    """
    page = callback_data.page

    data, count = await UserService().get_admins(page=page)

    text = localize_text_to_message(text_in_yaml="message_to_admin_menu", lang=user.language_code, count=str(count))
    keyboard = await keyboard_generator.generate_dynamic_keyboard(
        kb_key="admin_menu", data=data, lang=user.language_code, count=count, page=page
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@admin_router.callback_query(AdminManageData.filter())
async def select_admin_menu_handler(
    callback: CallbackQuery, callback_data: AdminManageData, user: UserSchema, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the callback query for selecting an admin menu in an admin management system.

    :param callback: CallbackQuery object containing information about the user interaction.
    :type callback: CallbackQuery
    :param callback_data: AdminManageData object containing additional data sent with the callback.
    :type callback_data: AdminManageData
    :param user: UserSchema object representing the currently logged-in user.
    :type user: UserSchema
    :param keyboard_generator: KeyboardGenerator instance used to generate and send keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    admin = await UserService().get_user(user_id=callback_data.id)

    kb_key = "select_admin_menu"
    message_key = "message_to_select_admin_menu"
    if admin.telegram_id == callback.from_user.id:
        kb_key = "select_self_admin_menu"
        message_key = "message_to_select_self_admin_menu"

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
        telegram_id=str(admin.telegram_id),
        full_name=admin.full_name,
        username=admin.username,
    )

    keyboard = await keyboard_generator.generate_static_keyboard(kb_key=kb_key, lang=user.language_code, id=admin.id)

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@admin_router.callback_query(AdminRemoveData.filter())
async def remove_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: AdminRemoveData,
    user: UserSchema,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the callback query for removing an admin in an admin management system.

    :param callback: The callback query received from the user.
    :type callback: CallbackQuery
    :param callback_data: Data associated with the callback query.
    :type callback_data: AdminRemoveData
    :param user: User schema containing user information.
    :type user: UserSchema
    :param keyboard_generator: A generator for creating keyboard layouts.
    :type keyboard_generator: KeyboardGenerator
    """
    text = localize_text_to_message(text_in_yaml="message_to_remove_admin_menu", lang=user.language_code)

    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="remove_admin_menu", lang=user.language_code, id=callback_data.id
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@admin_router.callback_query(AdminRemoveConfirmData.filter())
async def confirm_remove_admin_handler(
    callback: CallbackQuery,
    callback_data: AdminRemoveConfirmData,
    user: UserSchema,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the callback query for confirming removes an admin management system.

    :param callback: The callback query received from the user.
    :type callback: CallbackQuery
    :param callback_data: Data extracted from the callback query, containing information about the user to be removed.
    :type callback_data: AdminRemoveConfirmData
    :param user: Schema representing the current user performing the action.
    :type user: UserSchema
    :param keyboard_generator: Utility for generating dynamic and static keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    await UserService().update_user(user_id=callback_data.id, field="is_admin", value=False)

    text = localize_text_to_message(text_in_yaml="message_to_confirm_remove_admin_menu", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="remove_admin_confirm_menu", lang=user.language_code
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@admin_router.callback_query(AdminAddData.filter())
async def add_admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard_generator: KeyboardGenerator, state: FSMContext
) -> None:
    """
    Handles the callback query to add an admin menu.

    :param callback: The callback query received from the user.
    :type callback: CallbackQuery
    :param user: User schema containing user-specific data.
    :type user: UserSchema
    :param keyboard_generator: Utility for generating keyboards.
    :type keyboard_generator: KeyboardGenerator
    :param state: Finite State Machine context for managing states.
    :type state: FSMContext
    """
    text = localize_text_to_message(text_in_yaml="message_to_add_admin_menu", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="add_admin_menu", lang=user.language_code, request_id=randint(1, 10000000)
    )

    msg = await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        del_prev=True,
    )
    await state.update_data({"message_id": msg.message_id})
    await state.set_state(ShareUsersSteps.WAIT_USERS)


@admin_router.message(lambda message: message.users_shared, StateFilter(ShareUsersSteps.WAIT_USERS))
async def add_admin_share_handler(
    message: Message, user: UserSchema, state: FSMContext, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the addition of administrators by processing shared users.

    :param message: The incoming Telegram message containing shared users information.
    :type message: Message
    :param user: User schema object containing user-specific details.
    :type user: UserSchema
    :param state: Finite State Machine context to manage and store current state.
    :type state: FSMContext
    :param keyboard_generator: Keyboard generator instance to create interactive keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    admins_list, bot_link = await UserService().save_admins(users=message.users_shared.users)

    if admins_list:
        text = localize_text_to_message(
            text_in_yaml="message_to_add_admin_confirm",
            lang=user.language_code,
            admins_list=admins_list,
            bot_link=bot_link,
        )
    else:
        text = localize_text_to_message(text_in_yaml="message_to_add_admin_empty", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(kb_key="add_admin_confirm", lang=user.language_code)
    message_id = await state.get_value("message_id")

    await send_message(
        chat_id=message.chat.id,
        message_id=message_id,
        del_prev=True,
        text=text,
        reply_markup=keyboard,
    )

    await state.clear()
