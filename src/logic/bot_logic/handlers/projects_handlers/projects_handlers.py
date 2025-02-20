from aiogram import F, Router
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.EditProject import (
    ConfirmAction,
    ConfirmActionFAT,
    ConfirmEditTargetPath,
    EditProject,
    EditProjectFAT,
    EditTargetPath,
    ProjectType,
)
from src.entities.enums.edit_action_type_enum import EditActionTypeEnum
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.text_utils import format_text_with_kwargs

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
    result_text = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_projects_menu")
    )
    await callback.message.edit_text(
        text=result_text,
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
    result_text = format_text_with_kwargs(Configuration.strings.get("messages_text").get("message_to_add_project_menu"))
    await callback.message.edit_text(
        text=result_text,
        reply_markup=keyboard.create_static_keyboard(key="add_project_menu_keyboard", lang="en"),
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.add == F.action_type) & ("true" == F.confirmed_action))
)
async def confirm_add_project_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAction,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ConfirmAction

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(callback_data)
    project_id = 1
    project_name = "example"
    result_text = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_add_project_confirm_menu"),
        project_name=project_name,
    )
    await callback.message.edit_text(
        text=result_text,
        reply_markup=keyboard.create_static_keyboard(
            key="confirm_add_project_menu_keyboard", lang=user.language_code, placeholder={"id": project_id}
        ),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.edit == F.action_type))
async def edit_project_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProject

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(callback.data)
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_edit_project_menu"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_project_menu", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
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


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.edit_following_action_type == F.action_type))
async def edit_project_following_action_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the edit project following action query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProject

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_type_following_actions"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_keyboard", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
    )


@projects_router.callback_query(EditTargetPath.filter())
async def edit_fat_edit_target_path(
    callback: CallbackQuery,
    callback_data: EditTargetPath,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit of a target path (CHAT_ID or THREAD_ID) from any event type in project activities.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditTargetPath

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(f"callback_data: {callback_data}")
    current_target_id = 1
    result_text = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_edit_target_path"),
        target_action_type=callback_data.target_action_type.value,
        current_id=current_target_id,
    )

    await callback.message.edit_text(
        text=result_text,
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_edit_target_path_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "target_action_type": callback_data.target_action_type.value,
                "fat_event_type": callback_data.fat_event_type.value,
            },
        ),
    )


@projects_router.callback_query(ConfirmEditTargetPath.filter())
async def edit_fat_edit_target_path_confirm(
    callback: CallbackQuery,
    user: UserSchema,
    callback_data: EditTargetPath,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Confirms the edit of a target path (CHAT_ID or THREAD_ID) from any event type in project activities.

    :param callback: The callback query object containing user interaction data.
    :type callback: CallbackQuery

    :param user: The schema representing the current user.
    :type user: UserSchema

    :param callback_data: Data associated with the confirmation of editing the target path.
    :type callback_data: EditTargetPath

    :param keyboard: A keyboard generator for creating and manipulating reply keyboards (default is a new instance).
    :type keyboard: KeyboardGenerator

    :raises ValueError: If there are issues in formatting the result text or handling user data.
    """
    current_target_id = 1
    old_target_id = 101
    result_text = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_edit_target_path_confirm"),
        target_action_type=callback_data.target_action_type.value,
        current_id=current_target_id,
        old_id=old_target_id,
    )

    await callback.message.edit_text(
        text=result_text, reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang=user.language_code)
    )


@projects_router.callback_query(EditProjectFAT.filter(EventTypeEnum.epic == F.fat_event_type))
async def edit_fat_epic_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (epic) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProjectFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_fat_epic"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_epic_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type.value},
        ),
    )


@projects_router.callback_query(EditProjectFAT.filter(EventTypeEnum.milestone == F.fat_event_type))
async def edit_fat_milestone_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (milestone) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProjectFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_fat_milestone"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_milestone_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type.value},
        ),
    )


@projects_router.callback_query(EditProjectFAT.filter(EventTypeEnum.userstory == F.fat_event_type))
async def edit_fat_user_story_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (userstory) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProjectFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_fat_user_story"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_user_story_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type.value},
        ),
    )


@projects_router.callback_query(EditProjectFAT.filter(EventTypeEnum.task == F.fat_event_type))
async def edit_fat_task_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (task) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProjectFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_fat_task"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_task_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type.value},
        ),
    )


@projects_router.callback_query(EditProjectFAT.filter(EventTypeEnum.issue == F.fat_event_type))
async def edit_fat_issue_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (issue) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProjectFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_edit_fat_issue"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_issue_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type.value},
        ),
    )


@projects_router.callback_query(EditProjectFAT.filter(EventTypeEnum.wikipage == F.fat_event_type))
async def edit_fat_wikipage_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (wiki page) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProjectFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        text=Configuration.strings.get("messages_text").get("message_to_edit_fat_wikipage"),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_wikipage_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type.value},
        ),
    )


@projects_router.callback_query(ConfirmActionFAT.filter())
async def edit_fat_event_confirm(
    callback: CallbackQuery,
    callback_data: ConfirmActionFAT,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ConfirmActionFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    project_name = "example"
    type_status_current = "off"
    type_status_new = "on"
    result_text = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_edit_fat_confirm"),
        fat_event_type=callback_data.fat_event_type.value,
        project_name=project_name,
        type_status_current=type_status_current,
        type_status_new=type_status_new,
    )

    await callback.message.edit_text(
        text=result_text,
        reply_markup=keyboard.create_static_keyboard(
            key="started_keyboard",
            lang=user.language_code,
            placeholder={"id": callback_data.id, "fat_event_type": callback_data.fat_event_type},
        ),
    )


@projects_router.callback_query(EditProject.filter(EditActionTypeEnum.remove == F.action_type))
async def remove_project_menu_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditProject

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_remove_project_menu"),
        reply_markup=keyboard.create_static_keyboard(
            key="remove_project", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
    )


@projects_router.callback_query(ConfirmAction.filter(EditActionTypeEnum.remove == F.action_type))
async def remove_project_confirm_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAction,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ConfirmAction

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await callback.message.edit_text(
        Configuration.strings.get("messages_text").get("message_to_remove_project_confirm"),
        reply_markup=keyboard.create_static_keyboard(
            key="started_keyboard", lang=user.language_code, placeholder={"id": callback_data.id}
        ),
    )


# TODO: в информации по созданному проекту выводить permalink для webhook
# TODO: переделать структуру главного меню проектов, используя create_dynamic_keyboard
# TODO: проверить как будет вести себя генератор клавиатуры, если не будет key_in_storage > добиться опциональности
