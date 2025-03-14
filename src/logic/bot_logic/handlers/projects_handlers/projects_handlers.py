from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import get_logger
from src.entities.callback_classes.checkbox_callbacks import CheckboxData
from src.entities.callback_classes.project_callbacks import (
    AddProject,
    AddProjectInstance,
    ChangeInstanceName,
    ConfirmAddInstance,
    ConfirmChangeInstanceName,
    ConfirmEditInstanceChatID,
    ConfirmEditInstanceThreadID,
    ConfirmProjectEditName,
    ConfirmRemoveInstance,
    ConfirmRemoveProject,
    EditInstanceChatID,
    EditInstanceFAT,
    EditInstanceThreadID,
    EditProjectInstance,
    InstanceTargetPath,
    ProjectAddedConfirm,
    ProjectEditName,
    ProjectID,
    ProjectInstanceID,
    ProjectMenuData,
    RemoveInstance,
    RemoveProject,
)
from src.entities.enums.edit_action_type_enum import ProjectsCommonMenuEnum
from src.entities.enums.event_enums import EventTypeEnum
from src.entities.schemas.project_data.project_schemas import InstanceCreateModel
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.entities.states.project_states import (
    InstanceEditChatIDState,
    InstanceEditNameState,
    InstanceEditThreadIDState,
    InstanceNameState,
    ProjectEditNameState,
    ProjectNameState,
)
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.logic.services.project_service import ProjectService
from src.utils.send_message_utils import send_message
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
    project, created = await ProjectService().get_or_create_project(name=name)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="confirm_add_project_menu_keyboard",
        lang=user.language_code,
        id=project.id,
    )
    await send_message(
        chat_id=message.chat.id,
        message_id=await state.get_value("message_id"),
        del_prev=True,
        text=text,
        reply_markup=keyboard,
    )
    logger.debug(f"project {project.id}")
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
    state: FSMContext,
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

    :param state: The current state.
    :type state: FSMContext
    """
    logger.debug(callback.data)
    project_id = callback_data.id
    await state.update_data(project_id=project_id)
    text = localize_text_to_message(text_in_yaml="message_edit_project_menu", lang=user.language_code)
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
    keyboard_generator: KeyboardGenerator,
    state: FSMContext,
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: ProjectEditName

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator

    :param state: The current state.
    :type state: FSMContext
    """
    text = localize_text_to_message(text_in_yaml="message_to_edit_project_name", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_project_name_keyboard", lang=user.language_code, id=callback_data.id
    )

    await state.set_state(ProjectEditNameState.WAIT_NAME)
    await state.update_data(project_id=callback_data.id)

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.message(StateFilter(ProjectEditNameState.WAIT_NAME))
async def wait_input_edit_project_name_handler(
    message: Message,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    new_project_name = message.text
    await state.update_data(new_project_name=new_project_name)
    project_id = await state.get_value("project_id")
    text = localize_text_to_message(
        text_in_yaml="message_after_input_project_name", lang=user.language_code, new_project_name=new_project_name
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="after_input_project_name_keyboard",
        lang=user.language_code,
        id=project_id,
    )
    await send_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
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
    project = await ProjectService().get_project(project_id=callback_data.id)
    old_project_name = project.name
    new_project_name = await state.get_value("new_project_name")
    await ProjectService().update_project_name(project_id=callback_data.id, new_name=new_project_name)
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
    await state.set_state(None)
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


@projects_router.callback_query(ConfirmRemoveProject.filter())
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
        kb_key="confirm_remove_project_keyboard", lang=user.language_code, id=callback_data.id
    )
    await ProjectService().delete_project(project_id=callback_data.id)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(EditProjectInstance.filter())
async def edit_project_instances_handler(
    callback: CallbackQuery,
    callback_data: EditProjectInstance,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the instance menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback data that triggered the handler.
    :type callback_data: EditProjectInstance

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
        :type keyboard_generator: KeyboardGenerator
    """
    # TODO: реализовать метод для получения инстанса из БД
    data, count = await ProjectService().get_paginated_instances(project_id=callback_data.id, page=callback_data.page)
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


@projects_router.callback_query(AddProjectInstance.filter())
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
    kb_key = "add_instance_keyboard"
    message_key = "message_to_add_instance_in_project"
    project_id = await state.get_value("project_id")

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
    )

    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key=kb_key,
        lang=user.language_code,
    )
    msg = await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )
    await state.update_data({"message_id": msg.message_id, "project_id": project_id})
    await state.set_state(InstanceNameState.WAIT_INSTANCE_NAME)


@projects_router.message(StateFilter(InstanceNameState.WAIT_INSTANCE_NAME))
async def add_name_instance_handler(
    message: Message,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    name = message.text
    await state.update_data(instance_name=name)
    text = localize_text_to_message(
        text_in_yaml="message_to_confirm_add_instance_in_project",
        lang=user.language_code,
        instance_name=name,
    )
    project_id = await state.get_value("project_id")
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="confirm_add_instance_keyboard",
        lang=user.language_code,
        id=project_id,
    )
    await send_message(
        chat_id=message.chat.id,
        message_id=await state.get_value("message_id"),
        del_prev=True,
        text=text,
        reply_markup=keyboard,
    )
    await state.set_state(None)


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
    project_id = callback_data.id
    instance_name = await state.get_value("instance_name")
    instance = InstanceCreateModel(instance_name=instance_name, language=user.language_code)
    await ProjectService().add_new_instance(project_id=project_id, new_instance=instance)
    instance = await ProjectService().get_instance_by_name(project_id=project_id, instance_name=instance_name)
    text = localize_text_to_message(text_in_yaml="message_after_add_instance_in_project", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_project_confirm_add_instance_keyboard",
        lang=user.language_code,
        instance_id=instance.instance_id,
    )
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
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
    project_id = await state.get_value("project_id")
    project = await ProjectService().get_project(project_id=project_id)
    instance = await ProjectService().get_instance(project_id=project_id, instance_id=callback_data.instance_id)
    text = localize_text_to_message(
        text_in_yaml="message_to_selected_instance_in_project",
        lang=user.language_code,
        project_name=project.name,
        instance_name=instance.instance_name,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_keyboard",
        lang=user.language_code,
        instance_id=callback_data.instance_id,
        id=project_id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ChangeInstanceName.filter())
async def change_instance_name_handler(
    callback: CallbackQuery,
    callback_data: ChangeInstanceName,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    project_id = await state.get_value("project_id")
    instance_id = callback_data.instance_id
    instance = await ProjectService().get_instance(project_id=project_id, instance_id=instance_id)
    current_instance_name = instance.instance_name
    text = localize_text_to_message(
        text_in_yaml="message_to_change_instance_name",
        lang=user.language_code,
        current_instance_name=current_instance_name,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="change_instance_name_keyboard",
        lang=user.language_code,
        instance_id=callback_data.instance_id,
    )
    await state.set_state(InstanceEditNameState.WAIT_INSTANCE_NAME)
    await state.update_data(instance_id=callback_data.instance_id)
    await state.update_data(current_instance_name=current_instance_name)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.message(StateFilter(InstanceEditNameState.WAIT_INSTANCE_NAME))
async def wait_change_instance_name_handler(
    message: Message,
    user: UserSchema,
    keyboard_generator: KeyboardGenerator,
    state: FSMContext,
):
    new_instance_name = message.text
    instance_id = await state.get_value("instance_id")

    text = localize_text_to_message(
        text_in_yaml="message_after_change_instance_name", lang=user.language_code, new_instance_name=new_instance_name
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="after_input_change_instance_name_keyboard",
        lang=user.language_code,
        instance_id=instance_id,
    )

    await state.update_data(new_instance_name=new_instance_name)
    await send_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmChangeInstanceName.filter())
async def confirm_change_instance_name_handler(
    callback: CallbackQuery,
    callback_data: ConfirmChangeInstanceName,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    project_id = await state.get_value("project_id")
    new_instance_name = await state.get_value("new_instance_name")
    current_instance_name = await state.get_value("current_instance_name")
    instance_id = await state.get_value("instance_id")

    text = localize_text_to_message(
        text_in_yaml="message_to_confirm_change_instance_name",
        lang=user.language_code,
        current_instance_name=current_instance_name,
        new_instance_name=new_instance_name,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="change_instance_name_keyboard",
        lang=user.language_code,
        instance_id=instance_id,
    )
    await ProjectService().update_instance(
        project_id=project_id, instance_id=instance_id, field="instance_name", value=new_instance_name
    )
    await state.set_state(None)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
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
    :type callback_data: ProjectSelectedMenu

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    kb_key = "edit_fat_keyboard"
    message_key = "message_to_edit_type_following_actions"
    instance_id = callback_data.instance_id
    project_id = await state.get_value("project_id")
    await state.update_data({"instance_id": instance_id, "project_id": project_id})
    fats = await ProjectService().get_fat_list(project_id=project_id, instance_id=instance_id)
    selected_ids = [index for index, value in enumerate(list(EventTypeEnum)) if value in fats]
    print(selected_ids)
    logger.debug(f"instance_id: {instance_id}, project_id: {project_id}")

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
    )
    keyboard = await keyboard_generator.generate_checkbox_keyboard(
        kb_key=kb_key, selected_ids=selected_ids, lang=user.language_code, ok_button_text="confirm"
    )
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(CheckboxData.filter())
async def edit_project_following_action_checkbox_handler(
    callback: CallbackQuery,
    callback_data: CheckboxData,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the edit project following action query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectSelectedMenu

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    project_id = await state.get_value("project_id")
    instance_id = await state.get_value("instance_id")
    action = callback_data.action
    selected_ids = eval(callback_data.selected_ids)
    project = await ProjectService().get_project(project_id=project_id)
    project_name = project.name
    instance = await ProjectService().get_instance(project_id=project_id, instance_id=instance_id)
    instance_name = instance.instance_name

    message_key = "message_to_edit_type_following_actions"
    keyboard = await keyboard_generator.generate_checkbox_keyboard(
        kb_key="edit_fat_keyboard", selected_ids=selected_ids, lang=user.language_code, ok_button_text="confirm"
    )

    if action == "confirm":
        if selected_ids:
            message_key = "message_to_selected_instance_in_project"
            fats = [value for index, value in enumerate(list(EventTypeEnum)) if index in selected_ids]
            await ProjectService().update_instance_fat(project_id=project_id, instance_id=instance_id, fat=fats)
            keyboard = await keyboard_generator.generate_static_keyboard(
                kb_key="edit_instance_keyboard",
                lang=user.language_code,
                id=project_id,
                instance_id=instance_id,
            )

    text = localize_text_to_message(
        text_in_yaml=message_key,
        lang=user.language_code,
        project_name=project_name,
        instance_name=instance_name,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(InstanceTargetPath.filter())
async def edit_instance_target_path_handler(
    callback: CallbackQuery,
    callback_data: InstanceTargetPath,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    """
    Handles the edit project following action query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param callback_data: The callback query that triggered the handler.
    :type callback_data: ProjectSelectedMenu

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The current state.
    :type state: FSMContext

    :param keyboard_generator: A generator for creating keyboards.
    :type keyboard_generator: KeyboardGenerator
    """

    text = localize_text_to_message(text_in_yaml="message_to_edit_instance_target_path", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_target_path_keyboard",
        lang=user.language_code,
        instance_id=callback_data.instance_id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(EditInstanceChatID.filter())
async def edit_instance_chat_id_handler(
    callback: CallbackQuery,
    callback_data: EditInstanceChatID,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    # TODO: реализовать CRUD получения chat_id
    current_chat_id = ...
    text = localize_text_to_message(
        text_in_yaml="message_to_edit_instance_chat_id", lang=user.language_code, current_chat_id=current_chat_id
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_chat_id_keyboard", lang=user.language_code, instance_id=callback_data.instance_id
    )

    await state.set_state(InstanceEditChatIDState.WAIT_INSTANCE_CHAT_ID)
    await state.update_data(instance_id=callback_data.instance_id)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


@projects_router.message(StateFilter(InstanceEditChatIDState.WAIT_INSTANCE_CHAT_ID))
async def wait_edit_instance_chat_id_handler(
    message: Message,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    new_chat_id = message.text
    instance_id = await state.get_value("instance_id")
    await state.update_data(new_chat_id=new_chat_id)

    text = localize_text_to_message(
        text_in_yaml="message_to_wait_edit_instance_chat_id", lang=user.language_code, new_chat_id=new_chat_id
    )

    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="wait_input_instance_chat_id_keyboard",
        lang=user.language_code,
        instance_id=instance_id,
    )

    await send_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmEditInstanceChatID.filter())
async def confirm_edit_instance_chat_id_handler(
    callback: CallbackQuery,
    callback_data: ConfirmEditInstanceChatID,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    # TODO: реализовать CRUD получения chat_id
    current_chat_id = ...
    new_chat_id = await state.get_value("new_chat_id")

    text = localize_text_to_message(
        text_in_yaml="message_to_confirm_edit_chat_id",
        lang=user.language_code,
        current_chat_id=current_chat_id,
        new_chat_id=new_chat_id,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_chat_id_keyboard", lang=user.language_code, instance_id=callback_data.instance_id
    )

    await state.set_state(None)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


@projects_router.callback_query(EditInstanceThreadID.filter())
async def edit_instance_thread_id_handler(
    callback: CallbackQuery,
    callback_data: EditInstanceThreadID,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    # TODO: реализовать CRUD получения thread_id
    current_thread_id = ...
    text = localize_text_to_message(
        text_in_yaml="message_to_edit_instance_thread_id", lang=user.language_code, current_thread_id=current_thread_id
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_thread_id_keyboard", lang=user.language_code, instance_id=callback_data.instance_id
    )

    await state.set_state(InstanceEditThreadIDState.WAIT_INSTANCE_THREAD_ID)
    await state.update_data(instance_id=callback_data.instance_id)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


@projects_router.message(StateFilter(InstanceEditThreadIDState.WAIT_INSTANCE_THREAD_ID))
async def wait_edit_instance_thread_id_handler(
    message: Message,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    new_thread_id = message.text
    instance_id = await state.get_value("instance_id")
    await state.update_data(new_thread_id=new_thread_id)

    text = localize_text_to_message(
        text_in_yaml="message_to_wait_edit_instance_thread_id", lang=user.language_code, new_thread_id=new_thread_id
    )

    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="wait_input_instance_thread_id_keyboard",
        lang=user.language_code,
        instance_id=instance_id,
    )

    await send_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmEditInstanceThreadID.filter())
async def confirm_edit_instance_thread_id_handler(
    callback: CallbackQuery,
    callback_data: ConfirmEditInstanceThreadID,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    # TODO: реализовать CRUD получения chat_id
    current_thread_id = ...
    new_thread_id = await state.get_value("new_thread_id")

    text = localize_text_to_message(
        text_in_yaml="message_to_confirm_edit_thread_id",
        lang=user.language_code,
        current_thread_id=current_thread_id,
        new_thread_id=new_thread_id,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="edit_instance_thread_id_keyboard", lang=user.language_code, instance_id=callback_data.instance_id
    )

    await state.set_state(None)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
    )


@projects_router.callback_query(RemoveInstance.filter())
async def remove_instance_handler(
    callback: CallbackQuery,
    callback_data: RemoveInstance,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    # TODO: реализовать получение имени
    instance_name = ...
    project_name = ...

    text = localize_text_to_message(
        text_in_yaml="message_to_remove_instance",
        lang=user.language_code,
        instance_name=instance_name,
        project_name=project_name,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="remove_instance_keyboard", lang=user.language_code, instance_id=callback_data.instance_id
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )


@projects_router.callback_query(ConfirmRemoveInstance.filter())
async def confirm_remove_instance_handler(
    callback: CallbackQuery,
    callback_data: ConfirmRemoveInstance,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
):
    # TODO: реализовать получение имени
    project_name = ...
    instance_name = ...
    project_id = await state.get_value("project_id")
    logger.debug(f"project_id={project_id}")
    # TODO: реализовать удаление (нужен CRUD)
    ...

    text = localize_text_to_message(
        text_in_yaml="message_to_confirm_remove_instance",
        lang=user.language_code,
        instance_name=instance_name,
        project_name=project_name,
    )
    keyboard = await keyboard_generator.generate_static_keyboard(
        kb_key="confirm_remove_instance_keyboard_keyboard",
        lang=user.language_code,
        instance_id=callback_data.instance_id,
    )

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text,
        reply_markup=keyboard,
        try_to_edit=True,
    )
