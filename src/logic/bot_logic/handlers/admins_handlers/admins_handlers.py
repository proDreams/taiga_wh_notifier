from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.AdminActions import (
    AdminType,
    ConfirmAdminAction,
    SelectAdmin,
)
from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.state_utils import get_info_for_state
from src.utils.text_utils import localize_text_to_message

admin_router = Router()

logger = Configuration.logger.get_logger(name=__name__)

admin_test_keyboard_data = {
    "keyboard_type": "inline",  # select a type of a keyboards
    "row_width": [1, 1, 1, 1, 1],
    # Creates a layout scheme for entity elements (such as an event or an admin).
    # The number of digits indicates the number of entity rows (excluding pagination and fixed rows), while the digit
    # values specify the allowed number of elements per row.
    "fixed_top": [
        {"text": " ", "type": "callback", "data": "noop"},
        {"text": "Admin menu", "type": "callback", "data": "noop"},
        {"text": " ", "type": "callback", "data": "noop"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.
    "button": [
        {"text": "Gnidina", "type": "callback", "data": "admin:select:1"},
    ],
    #     The main array of buttons.
    "fixed_bottom": [
        {"text": "Back to menu", "type": "callback", "data": "{previous_callback}"},
        {"text": "Add admin", "type": "callback", "data": "admin:add"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.
}


@admin_router.callback_query(
    AdminType.filter(AdminActionTypeEnum.menu == F.action_type), StateFilter(SingleState.active)
)
async def admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The incoming user object.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_admin_menu", lang=user.language_code),
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=admin_test_keyboard_data,
            lang=user.language_code,
            key_in_storage="admin_test_keyboard_data",
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(AdminType.filter(AdminActionTypeEnum.add == F.action_type))
async def add_admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the add admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The incoming user object.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_add_admin_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(key="add_admin_menu", lang=user.language_code),
        try_to_edit=True,
    )


@admin_router.callback_query(
    ConfirmAdminAction.filter((AdminActionTypeEnum.add == F.action_type) & ("true" == F.confirmed_action))
)
async def confirm_add_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAdminAction,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the add admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ConfirmAdminAction

    :param user: The incoming user object.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_add_admin_confirm", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="started_keyboard", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(SelectAdmin.filter(AdminActionTypeEnum.select == F.action_type))
async def select_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: SelectAdmin,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the add admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: SelectAdmin

    :param user: The incoming user object.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_select_admin_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="select_admin_menu", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(SelectAdmin.filter(AdminActionTypeEnum.remove == F.action_type))
async def remove_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: SelectAdmin,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the remove admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: SelectAdmin

    :param user: The incoming user object.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_remove_admin_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="remove_admin_menu", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(
    ConfirmAdminAction.filter((AdminActionTypeEnum.remove == F.action_type) & ("true" == F.confirmed_action))
)
async def confirm_remove_admin_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAdminAction,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the confirm remove admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ConfirmAdminAction

    :param user: The incoming user object.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_confirm_remove_admin_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="started_keyboard", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
        try_to_edit=True,
    )
