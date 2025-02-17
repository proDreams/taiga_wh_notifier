from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.AdminActions import (
    AdminType,
    ConfirmAdminAction,
    SelectAdmin,
)
from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator

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
        {"text": "Back to menu", "type": "callback", "data": "menu"},
        {"text": "Add admin", "type": "callback", "data": "admin:add"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.
}


@admin_router.callback_query(AdminType.filter(AdminActionTypeEnum.menu == F.action_type))
# TODO: потом исправить callback
async def admin_menu_handler(
    callback: CallbackQuery,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_admin_menu"),
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=admin_test_keyboard_data,
            lang="en",
            key_in_storage="admin_test_keyboard_data",
        ),
    )


@admin_router.callback_query(AdminType.filter(AdminActionTypeEnum.add == F.action_type))
async def add_admin_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the add admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_add_admin_menu"),
        reply_markup=keyboard.create_static_keyboard(key="add_admin_menu", lang="en"),
    )


@admin_router.callback_query(
    ConfirmAdminAction.filter((AdminActionTypeEnum.add == F.action_type) & ("true" == F.confirmed_action))
)
async def confirm_add_admin_menu_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the add admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_add_admin_confirm"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )


@admin_router.callback_query(SelectAdmin.filter(AdminActionTypeEnum.select == F.action_type))
async def select_admin_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the add admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_select_admin_menu"),
        reply_markup=keyboard.create_static_keyboard(key="select_admin_menu", lang="en"),
    )


@admin_router.callback_query(SelectAdmin.filter(AdminActionTypeEnum.remove == F.action_type))
async def remove_admin_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the remove admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_remove_admin_menu"),
        reply_markup=keyboard.create_static_keyboard(key="remove_admin_menu", lang="en"),
    )


@admin_router.callback_query(
    ConfirmAdminAction.filter((AdminActionTypeEnum.remove == F.action_type) & ("true" == F.confirmed_action))
)
async def confirm_remove_admin_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the confirm remove admin menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_confirm_remove_admin_menu"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )
