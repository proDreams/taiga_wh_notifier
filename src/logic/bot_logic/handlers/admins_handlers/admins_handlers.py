from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.admin_callbacks import (
    AdminMenuData,
    AdminType,
    ConfirmAdminAction,
    SelectAdmin,
)
from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.logic.services.user_service import UserService
from src.utils.send_message_utils import send_message
from src.utils.state_utils import get_info_for_state
from src.utils.text_utils import localize_text_to_message

admin_router = Router()

logger = Configuration.logger.get_logger(name=__name__)


@admin_router.callback_query(AdminMenuData.filter())
async def admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard_generator: KeyboardGenerator, callback_data: AdminMenuData
) -> None:
    page = callback_data.page

    data, count = await UserService().get_admins(page=page)

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_admin_menu", lang=user.language_code),
        reply_markup=await keyboard_generator.generate_dynamic_keyboard(
            kb_key="admin_menu", data=data, lang=user.language_code, count=count, page=page
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(
    AdminType.filter(AdminActionTypeEnum.ADD == F.action_type), StateFilter(SingleState.active)
)
async def add_admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard_generator: KeyboardGenerator
) -> None:
    admin_id = "1"
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_add_admin_menu", lang=user.language_code),
        reply_markup=keyboard_generator.create_static_keyboard(
            key="add_admin_menu",
            lang=user.language_code,
            placeholder={
                "admin_id": admin_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(
    ConfirmAdminAction.filter((AdminActionTypeEnum.ADD == F.action_type) & ("t" == F.confirmed_action)),
    StateFilter(SingleState.active),
)
async def confirm_add_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAdminAction,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_add_admin_confirm", lang=user.language_code),
        reply_markup=keyboard_generator.create_static_keyboard(
            key="started_keyboard",
            lang=user.language_code,
            placeholder={
                "admin_id": callback_data.admin_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(
    SelectAdmin.filter(AdminActionTypeEnum.SELECT == F.action_type), StateFilter(SingleState.active)
)
async def select_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: SelectAdmin,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_select_admin_menu", lang=user.language_code),
        reply_markup=keyboard_generator.create_static_keyboard(
            key="select_admin_menu",
            lang=user.language_code,
            placeholder={
                "admin_id": callback_data.admin_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(
    SelectAdmin.filter(AdminActionTypeEnum.REMOVE == F.action_type), StateFilter(SingleState.active)
)
async def remove_admin_menu_handler(
    callback: CallbackQuery,
    callback_data: SelectAdmin,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_remove_admin_menu", lang=user.language_code),
        reply_markup=keyboard_generator.create_static_keyboard(
            key="remove_admin_menu",
            lang=user.language_code,
            placeholder={
                "admin_id": callback_data.admin_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )


@admin_router.callback_query(
    ConfirmAdminAction.filter((AdminActionTypeEnum.REMOVE == F.action_type) & ("t" == F.confirmed_action)),
    StateFilter(SingleState.active),
)
async def confirm_remove_admin_handler(
    callback: CallbackQuery,
    callback_data: ConfirmAdminAction,
    user: UserSchema,
    state: FSMContext,
    keyboard_generator: KeyboardGenerator,
) -> None:
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_confirm_remove_admin_menu", lang=user.language_code),
        reply_markup=keyboard_generator.create_static_keyboard(
            key="remove_admin_confirm_menu",
            lang=user.language_code,
            placeholder={
                "admin_id": callback_data.admin_id,
                "previous_callback": await get_info_for_state(callback=callback, state=state),
            },
        ),
        try_to_edit=True,
    )
