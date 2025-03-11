from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import get_logger
from src.entities.callback_classes.project_callbacks import (
    ActionEditTargetPath,
    AddProject,
    AddProjectInstance,
    ConfirmActionEditTargetPath,
    ConfirmActionFAT,
    ConfirmAddInstance,
    ConfirmProjectEditName,
    ConfirmRemoveProject,
    EditInstanceFAT,
    EditInstanceTargetPath,
    ProjectAddedConfirm,
    ProjectEditInstance,
    ProjectEditName,
    ProjectEventFAT,
    ProjectID,
    ProjectInstanceID,
    ProjectMenuData,
    ProjectTargetPath,
    RemoveProject,
)
from src.entities.enums.edit_action_type_enum import ProjectsCommonMenuEnum
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.entities.states.project_states import ProjectNameState
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.logic.services.project_service import ProjectService
from src.utils.send_message_utils import send_message
from src.utils.state_utils import get_info_for_state
from src.utils.text_utils import localize_text_to_message

projects_router = Router()

logger = get_logger(name=__name__)


@projects_router.callback_query(ProjectMenuData.filter())
async def projects_menu_handler(
    callback: CallbackQuery, callback_data: ProjectMenuData, user: UserSchema, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the project menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback: ProjectMenuData

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    text = localize_text_to_message(text_in_yaml="message_to_projects_menu", lang=user.language_code)
    data, count = await ProjectService().get_projects(page=callback_data.page)
    keyboard = await keyboard_generator.generate_dynamic_keyboard(
        kb_key="projects_menu",
        data=data,
        lang=user.language_code,
        page=callback_data.page,
        count=count,
    )
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(AddProject.filter())
async def add_project_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the callback query.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    text = localize_text_to_message(text_in_yaml="message_to_add_project_menu", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="add_project_menu_keyboard",
        lang=user.language_code,
    )
    msg = await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )
    await state.update_data({"message_id": msg.message_id})
    await state.set_state(ProjectNameState.WAIT_NAME)


@projects_router.message(StateFilter(ProjectNameState.WAIT_NAME))
async def add_name_handler(
    message: Message,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    name = message.text
    text = localize_text_to_message(
        text_in_yaml="message_add_project_confirm_menu",
        lang=user.language_code,
        project_name=name,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="confirm_add_project_menu_keyboard",
        lang=user.language_code,
        common_action_type=ProjectsCommonMenuEnum.EDIT,
        id="1",
    )
    project, created = await ProjectService().get_or_create_project(name=name)
    logger.info(f"project: {project}, created: {created}")
    await send_message(
        chat_id=message.chat.id,
        message_id=await state.get_value("message_id"),
        del_prev=True,
        text=text,
        reply_markup=keyboard,
    )
    await state.clear()


@projects_router.callback_query(
    ProjectAddedConfirm.filter((ProjectsCommonMenuEnum.ADD == F.common_action_type) & ("t" == F.confirmed_add)),
    StateFilter(SingleState.active),
)
async def confirm_add_project_handler(
    callback: CallbackQuery,
    callback_data: ProjectAddedConfirm,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
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

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    logger.info(callback_data)
    project_name = "example"

    text = localize_text_to_message(
        text_in_yaml="message_add_project_confirm_menu", lang=user.language_code, project_name=project_name
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="confirm_add_project_menu_keyboard",
        lang=user.language_code,
        id=callback_data.id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ProjectID.filter())
async def select_project_handler(
    callback: CallbackQuery,
    callback_data: ProjectID,
    keyboard_generator: KeyboardGenerator,
    user: UserSchema,
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectID

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    logger.debug(callback.data)

    text = localize_text_to_message(text_in_yaml="message_edit_project_menu", lang=user.language_code)

    # TODO: получение из бд списка
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="select_project_menu_keyboard",
        lang=user.language_code,
        id=callback_data.id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ProjectEditName.filter())
async def edit_project_name_menu_handler(
    callback: CallbackQuery,
    callback_data: ProjectEditName,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ProjectEditName

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
        :type keyboard: KeyboardGenerator
    """
    # TODO: тут надо будет уделить вниманию изменению имени (вызов message и передача через стейт)
    text = localize_text_to_message(text_in_yaml="message_to_edit_project_name", lang=user.language_code)
    keyboard = await keyboard.generate_static_keyboard(
        kb_key="edit_project_name_keyboard", lang=user.language_code, id=callback_data.id
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmProjectEditName.filter())
async def edit_project_name_confirm(
    callback: CallbackQuery,
    callback_data: ConfirmProjectEditName,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
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

    :param keyboard_generator: A generator for creating keyboards.
        :type keyboard_generator: KeyboardGenerator
    """
    # TODO: реализовать получение из стейта данных и запись в бд
    old_project_name = "OLD"
    new_project_name = "NEW"

    text = localize_text_to_message(
        text_in_yaml="message_to_edit_project_name_confirm",
        lang=user.language_code,
        old_project_name=old_project_name,
        new_project_name=new_project_name,
    )

    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_project_name_confirm_keyboard",
        lang=user.language_code,
        id=callback_data.id,
    )
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(RemoveProject.filter())
async def remove_project_menu_handler(
    callback: CallbackQuery,
    callback_data: RemoveProject,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: RemoveProject

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """

    text = localize_text_to_message(text_in_yaml="message_to_remove_project_menu", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="remove_project_keyboard",
        lang=user.language_code,
        id=callback_data.id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmRemoveProject.filter)
async def remove_project_confirm_handler(
    callback: CallbackQuery,
    callback_data: ConfirmRemoveProject,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ConfirmRemoveProject

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    text = localize_text_to_message(text_in_yaml="message_to_remove_project_confirm", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="remove_project_confirm_keyboard", lang=user.language_code, id=callback_data.id
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ProjectEditInstance.filter())
async def edit_project_instance_handler(
    callback: CallbackQuery,
    callback_data: ProjectEditInstance,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the instance menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ProjectSelectedMenu

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
        :type keyboard_generator: KeyboardGenerator
    """
    # TODO: реализовать метод для получения инстанса из БД
    data, count = ...

    text = localize_text_to_message(text_in_yaml="message_to_edit_instance_in_project", lang=user.language_code)
    keyboard = await keyboard_generator.generate_dynamic_keyboard(
        kb_key="select_instance_menu",
        lang=user.language_code,
        data=data,
        page=callback_data.page,
        count=count,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(AddProjectInstance.filter)
async def add_instance_handler(
    callback: CallbackQuery,
    callback_data: AddProjectInstance,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the instance menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ProjectInstanceAction

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    id_inst_from_result_crud = "1"

    text = localize_text_to_message(text_in_yaml="message_to_add_instance_in_project", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        key="edit_project_add_instance_keyboard",
        lang=user.language_code,
        inst_id=id_inst_from_result_crud,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        # TODO: здесь актуализировать сообщение
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmAddInstance.filter())
async def confirm_add_instance_action(
    callback: CallbackQuery,
    callback_data: ConfirmAddInstance,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the instance menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ConfirmAddInstance

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """

    text = localize_text_to_message(text_in_yaml="message_to_confirm_add_instance_in_project", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_project_confirm_add_instance_keyboard",
        lang=user.language_code,
        inst_id=callback_data.inst_id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        # TODO: здесь актуализировать сообщение
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ProjectInstanceID.filter())
async def edit_selected_instance_handler(
    callback: CallbackQuery,
    callback_data: ProjectInstanceID,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the instance menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ProjectInstanceID

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    text = localize_text_to_message(text_in_yaml="message_to_selected_instance_in_project", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_keyboard",
        lang=user.language_code,
        inst_id=callback_data.inst_id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        # TODO: здесь актуилизировать сообщение
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(EditInstanceFAT.filter())
async def edit_project_following_action_handler(
    callback: CallbackQuery,
    callback_data: EditInstanceFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the edit project following action query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: EditInstanceFAT

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    text = localize_text_to_message(text_in_yaml="message_to_edit_type_following_actions", lang=user.language_code)
    keyboard = await keyboard_generator.generate_
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(EditInstanceTargetPath.filter())
async def edit_instance_target_path_handler(
    callback: CallbackQuery,
    callback_data: EditInstanceTargetPath,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the edit instance target path query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectInstanceAction

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_edit_type_following_actions", lang=user.language_code),
        reply_markup=keyboard_generator.create_static_keyboard(
            key="edit_instance_type_target_path_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(ProjectTargetPath.filter(), StateFilter(SingleState.active))
async def edit_project_select_type_target_path(
    callback: CallbackQuery,
    callback_data: ProjectTargetPath,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit of a target path (CHAT_ID or THREAD_ID) from any event type in project activities.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectTargetPath

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
            key="edit_instance_target_path_select_action",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "target_action_type": callback_data.target_action_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(ActionEditTargetPath.filter(), StateFilter(SingleState.active))
async def edit_project_target_path_action(
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
            key="edit_instance_target_path_edit_action",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "target_action_type": callback_data.target_action_type.value,
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
            key="edit_instance_action_edit_target_path_confirm_keyboard",
            lang=user.language_code,
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectEventFAT.filter(EventTypeEnum.EPIC == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_fat_epic_event(
    callback: CallbackQuery,
    callback_data: ProjectEventFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (epic) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectEventFAT

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
            key="edit_instance_epic_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectEventFAT.filter(EventTypeEnum.MILESTONE == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_instance_milestone_event(
    callback: CallbackQuery,
    callback_data: ProjectEventFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (milestone) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectEventFAT

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
            key="edit_instance_milestone_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectEventFAT.filter(EventTypeEnum.USERSTORY == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_instance_user_story_event(
    callback: CallbackQuery,
    callback_data: ProjectEventFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (userstory) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectEventFAT

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
            key="edit_instance_user_story_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectEventFAT.filter(EventTypeEnum.TASK == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_instance_task_event(
    callback: CallbackQuery,
    callback_data: ProjectEventFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (task) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectEventFAT

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
            key="edit_instance_task_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectEventFAT.filter(EventTypeEnum.ISSUE == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_instance_issue_event(
    callback: CallbackQuery,
    callback_data: ProjectEventFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (issue) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectEventFAT

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
            key="edit_instance_issue_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(
    ProjectEventFAT.filter(EventTypeEnum.WIKIPAGE == F.fat_event_type), StateFilter(SingleState.active)
)
async def edit_instance_wikipage_event(
    callback: CallbackQuery,
    callback_data: ProjectEventFAT,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the changes edit following actions types (wiki page) query in project.
    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectEventFAT

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
            key="edit_instance_wikipage_keyboard",
            lang=user.language_code,
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmActionFAT.filter(), StateFilter(SingleState.active))
async def edit_instance_event_confirm(
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
            key="edit_instance_fat_confirm_keyboard",
            lang=user.language_code,
            # TODO: проверить необходимость плейсхолдера, вроде не нужен
            placeholder={
                "id": callback_data.id,
                "inst_id": callback_data.inst_id,
                "fat_event_type": callback_data.fat_event_type.value,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


# TODO: в информации по созданному проекту выводить permalink для webhook
# TODO: переделать структуру главного меню проектов, используя create_dynamic_keyboard
# TODO: проверить как будет вести себя генератор клавиатуры, если не будет key_in_storage > добиться опциональности


# @projects_router.callback_query()
# async def total_catcher(callback: CallbackQuery) -> None:
#     print(callback.data)
