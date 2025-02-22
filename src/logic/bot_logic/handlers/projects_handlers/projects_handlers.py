from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.project_callbacks import (
    ActionEditTargetPath,
    ConfirmAction,
    ConfirmActionEditTargetPath,
    ConfirmActionFAT,
    EditProject,
    EditProjectFAT,
    EditTargetPath,
    ProjectType,
)
from src.entities.enums.edit_action_type_enum import EditActionTypeEnum
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.state_utils import get_info_for_state
from src.utils.text_utils import localize_text_to_message

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
        {"text": "Test project", "type": "callback", "data": "prj:ed:1"},
    ],
    #     The main array of buttons.
    "fixed_bottom": [
        {"text": "Back to menu", "type": "callback", "data": "{previous_callback}"},
        {"text": "Add project", "type": "callback", "data": "prj:add"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.
}


@projects_router.callback_query(
    ProjectType.filter(EditActionTypeEnum.MENU == F.action_type), StateFilter(SingleState.active)
)
async def projects_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_projects_menu", lang=user.language_code),
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=test_project_menu_keyboard,
            lang=user.language_code,
            key_in_storage="test_project_menu_keyboard",
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectType.filter(EditActionTypeEnum.ADD == F.action_type), StateFilter(SingleState.active)
)
async def add_project_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_add_project_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="add_project_menu_keyboard",
            lang=user.language_code,
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.ADD == F.action_type) & ("t" == F.confirmed_action)),
    StateFilter(SingleState.active),
)
async def confirm_add_project_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAction,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(callback_data)
    project_id = 1
    project_name = "example"
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_add_project_confirm_menu", lang=user.language_code, project_name=project_name
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="confirm_add_project_menu_keyboard",
            lang=user.language_code,
            placeholder={
                "id": project_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProject.filter(EditActionTypeEnum.EDIT == F.action_type), StateFilter(SingleState.active)
)
async def edit_project_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.debug(callback.data)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_edit_project_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_project_menu",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProject.filter(EditActionTypeEnum.EDIT_NAME == F.action_type), StateFilter(SingleState.active)
)
async def edit_project_name_menu_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: EditProject

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_edit_project_name", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_project_name_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ConfirmAction.filter((EditActionTypeEnum.EDIT_NAME == F.action_type) & ("t" == F.confirmed_action)),
    StateFilter(SingleState.active),
)
async def edit_project_name_confirm(
    callback: CallbackQuery,
    callback_data: ConfirmAction,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    old_project_name = "OLD"
    new_project_name = "NEW"
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_project_name_confirm",
            lang=user.language_code,
            old_project_name=old_project_name,
            new_project_name=new_project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_project_name_confirm_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProject.filter(EditActionTypeEnum.EDIT_FOLLOWING_ACTION_TYPE == F.action_type), StateFilter(SingleState.active)
)
async def edit_project_following_action_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_edit_type_following_actions", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(EditTargetPath.filter(), StateFilter(SingleState.active))
async def edit_fat_edit_target_path(
    callback: CallbackQuery,
    callback_data: EditTargetPath,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(f"callback_data: {callback_data}")
    current_target_id = 1
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_target_path",
            lang=user.language_code,
            target_action_type=callback_data.target_action_type.value,
            current_id=str(current_target_id),
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_target_path_action",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "target_action_type": callback_data.target_action_type.value,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(ActionEditTargetPath.filter(), StateFilter(SingleState.active))
async def edit_fat_action_target_path(
    callback: CallbackQuery,
    callback_data: ActionEditTargetPath,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit of a target path (CHAT_ID or THREAD_ID) from any event type in project activities.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ActionEditTargetPath

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    logger.info(f"callback_data: {callback_data}")
    current_target_id = 1
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_target_path",
            lang=user.language_code,
            target_action_type=callback_data.target_action_type.value,
            current_id=str(current_target_id),
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_action_target_path",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "target_action_type": callback_data.target_action_type.value,
                "fat_event_type": callback_data.fat_event_type.value,
                "action_target_edit": callback_data.action_target_edit.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmActionEditTargetPath.filter(), StateFilter(SingleState.active))
async def edit_fat_edit_target_path_confirm(
    callback: CallbackQuery,
    callback_data: ConfirmActionEditTargetPath,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Confirms the edit of a target path (CHAT_ID or THREAD_ID) from any event type in project activities.

    :param callback: The callback query object containing user interaction data.
    :type callback: CallbackQuery

    :param callback_data: Data associated with the confirmation of editing the target path.
    :type callback_data: ConfirmActionEditTargetPath

    :param user: The schema representing the current user.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A keyboard generator for creating and manipulating reply keyboards (default is a new instance).
    :type keyboard: KeyboardGenerator

    :raises ValueError: If there are issues in formatting the result text or handling user data.
    """
    current_target_id = 1
    old_target_id = 101
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_target_path_confirm",
            lang=user.language_code,
            target_action_type=callback_data.target_action_type.value,
            current_id=str(current_target_id),
            old_id=str(old_target_id),
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_action_edit_target_path_confirm_keyboard",
            lang=user.language_code,
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProjectFAT.filter(EventTypeEnum.EPIC == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_epic_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    # TODO: заполнить корректными данными
    type_status_current = ...
    type_status_new = ...
    project_name = ...
    logger.info(f"callback_data: {callback_data}")
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_epic",
            lang=user.language_code,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
            project_name=project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_epic_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProjectFAT.filter(EventTypeEnum.MILESTONE == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_milestone_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    type_status_current = ...
    type_status_new = ...
    project_name = ...
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_milestone",
            lang=user.language_code,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
            project_name=project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_milestone_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProjectFAT.filter(EventTypeEnum.USERSTORY == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_user_story_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    type_status_current = ...
    type_status_new = ...
    project_name = ...
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_user_story",
            lang=user.language_code,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
            project_name=project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_user_story_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProjectFAT.filter(EventTypeEnum.TASK == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_task_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    type_status_current = ...
    type_status_new = ...
    project_name = ...
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_task",
            lang=user.language_code,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
            project_name=project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_task_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProjectFAT.filter(EventTypeEnum.ISSUE == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_issue_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    type_status_current = ...
    type_status_new = ...
    project_name = ...
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_issue",
            lang=user.language_code,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
            project_name=project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_issue_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProjectFAT.filter(EventTypeEnum.WIKIPAGE == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_wikipage_event(
    callback: CallbackQuery,
    callback_data: EditProjectFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    type_status_current = ...
    type_status_new = ...
    project_name = ...
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_wikipage",
            lang=user.language_code,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
            project_name=project_name,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_wikipage_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmActionFAT.filter(), StateFilter(SingleState.active))
async def edit_fat_event_confirm(
    callback: CallbackQuery,
    callback_data: ConfirmActionFAT,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    project_name = "example"
    type_status_current = "off"
    type_status_new = "on"
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(
            text_in_yaml="message_to_edit_fat_confirm",
            lang=user.language_code,
            fat_event_type=callback_data.fat_event_type.value,
            project_name=project_name,
            type_status_current=type_status_current,
            type_status_new=type_status_new,
        ),
        reply_markup=keyboard.create_static_keyboard(
            key="edit_fat_confirm_keyboard",
            lang=user.language_code,
            # TODO: проверить необходимость плейсхолдера, вроде не нужен
            placeholder={
                "id": callback_data.id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    EditProject.filter(EditActionTypeEnum.REMOVE == F.action_type), StateFilter(SingleState.active)
)
async def remove_project_menu_handler(
    callback: CallbackQuery,
    callback_data: EditProject,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_remove_project_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="remove_project_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ConfirmAction.filter(EditActionTypeEnum.REMOVE == F.action_type), StateFilter(SingleState.active)
)
async def remove_project_confirm_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAction,
    user: UserSchema,
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_remove_project_confirm", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="remove_project_confirm_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


# TODO: в информации по созданному проекту выводить permalink для webhook
# TODO: переделать структуру главного меню проектов, используя create_dynamic_keyboard
# TODO: проверить как будет вести себя генератор клавиатуры, если не будет key_in_storage > добиться опциональности
