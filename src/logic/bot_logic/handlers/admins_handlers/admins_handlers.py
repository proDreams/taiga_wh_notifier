from random import randint

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import Configuration
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

logger = Configuration.logger.get_logger(name=__name__)


@admin_router.callback_query(AdminMenuData.filter())
async def admin_menu_handler(
    callback: CallbackQuery, user: UserSchema, keyboard_generator: KeyboardGenerator, callback_data: AdminMenuData
) -> None:
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
    admins_list, bot_link = await UserService().save_admins(users=message.users_shared.users)

    text = localize_text_to_message(
        text_in_yaml="message_to_add_admin_confirm", lang=user.language_code, admins_list=admins_list, bot_link=bot_link
    )
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
