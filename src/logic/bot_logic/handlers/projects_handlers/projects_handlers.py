from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.EditProject import (
    ConfirmAction,
    EditProject,
    ProjectType,
)
from src.entities.enums.edit_action_type_enum import EditActionTypeEnum
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator

projects_router = Router()

logger = Configuration.logger.get_logger(name=__name__)

test_project_menu_keyboard = {
    "keyboard_type": "inline",  # select a type of a keyboards
    "row_width": [1, 1, 1, 1, 1],
    # Creates a layout scheme for entity elements (such as an event or an admin).
    # The number of digits indicates the number of entity rows (excluding pagination and fixed rows), while the digit
    # values specify the allowed number of elements per row.
    "fixed_top": [
        {"text": " ", "type": "callback", "data": "noop"},
        {"text": "Projects menu", "type": "callback", "data": "noop"},
        {"text": " ", "type": "callback", "data": "noop"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.
    "button": [
        {"text": "Test project", "type": "callback", "data": "project:edit:1"},
    ],
    #     The main array of buttons.
    "fixed_bottom": [
        {"text": "Back to menu", "type": "callback", "data": "menu"},
        {"text": "Add project", "type": "callback", "data": "project:add"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.
}


@projects_router.callback_query(ProjectType.filter(EditActionTypeEnum.menu == F.action_type))
async def projects_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    # TODO: пока оставим на всякий случай старую клавиатуру, после согласования уберем
    # await callback.message.edit_text(
    #     Configuration.strings.get("messages_text").get("message_to_projects_menu"),
    #     reply_markup=keyboard.create_static_keyboard(key="projects_menu", lang="en"),
    # )
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_projects_menu"),
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=test_project_menu_keyboard, key_in_storage="test_project_menu_keyboard", lang="en"
        ),
    )


@projects_router.callback_query(ProjectType.filter(EditActionTypeEnum.add == F.action_type))
async def add_project_menu_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_add_project_menu"),
        reply_markup=keyboard.create_static_keyboard(key="add_project_confirm", lang="en"),
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.add == F.action_type) & ("true" == F.confirmed_action))
)
async def confirm_add_project_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_add_project_confirm_menu"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.edit == F.action_type))
async def edit_project_handler(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(callback.data)
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_edit_project_menu"),
        reply_markup=keyboard.create_static_keyboard(key="edit_project_menu", lang="en"),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.edit_name == F.action_type))
async def edit_project_name_menu_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_project_name"),
        reply_markup=keyboard.create_static_keyboard(key="edit_project_name", lang="en"),
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.edit_name == F.action_type) & ("true" == F.confirmed_action))
)
async def edit_project_name_confirm(callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_project_name_confirm"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.edit_chat_id == F.action_type))
async def edit_project_chat_id_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_project_chat_id"),
        reply_markup=keyboard.create_static_keyboard(key="edit_project_chat_id_keyboard", lang="en"),
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.edit_chat_id == F.action_type) & ("true" == F.confirmed_action))
)
async def edit_project_chat_id_confirm_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_project_chat_id_confirm"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.edit_thread_id == F.action_type))
async def edit_project_thread_id_menu_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_project_thread_id"),
        reply_markup=keyboard.create_static_keyboard(key="edit_project_thread_id", lang="en"),
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.edit_thread_id == F.action_type) & ("true" == F.confirmed_action))
)
async def edit_project_thread_id_confirm_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_project_thread_id_confirm"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.remove == F.action_type))
async def remove_project_menu_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_remove_project_menu"),
        reply_markup=keyboard.create_static_keyboard(key="remove_project", lang="en"),
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.remove == F.action_type) & ("true" == F.confirmed_action))
)
async def remove_project_confirm_handler(
    callback: CallbackQuery, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_remove_project_confirm"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )


# TODO: в информации по созданному проекту выводить permalink для webhook
# TODO: переделать структуру главного меню проектов, используя create_dynamic_keyboard
# TODO: проверить как будет вести себя генератор клавиатуры, если не будет key_in_storage > добиться опциональности
