from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import Configuration
from src.entities.callback_classes.menu_callbacks import MenuData
from src.entities.enums.handlers_enum import CommandsEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.logic.bot_logic.filters.menu_command_filter import MenuCommandFilter
from src.logic.bot_logic.handlers.admins_handlers import admin_router
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.text_utils import localize_text_to_message

logger = Configuration.logger.get_logger(name=__name__)

main_router = Router()


@main_router.message(Command(commands=[CommandsEnum.START]))
async def start_handler(
    message: Message, state: FSMContext, user: UserSchema, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the start command by sending an initial message to the user and clearing any previous state.

    :param message: The incoming message from the user.
    :type message: Message
    :param state: The current state of the FSM (Finite State Machine).
    :type state: FSMContext
    :param user: The schema representing the user's data, including language preferences.
    :type user: UserSchema
    :param keyboard_generator: The generator used to create dynamic or static keyboards.
    :type keyboard_generator: KeyboardGenerator
    """
    await state.clear()

    text = localize_text_to_message(text_in_yaml="message_to_start", lang=user.language_code)
    keyboard = await keyboard_generator.generate_static_keyboard(kb_key="start_keyboard", lang=user.language_code)

    await send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)


@admin_router.message(MenuCommandFilter())
@main_router.callback_query(MenuData.filter())
async def main_menu_handler(
    message: CallbackQuery | Message, user: UserSchema, state: FSMContext, keyboard_generator: KeyboardGenerator
) -> None:
    """
    Handles the main menu display and interaction for users.

    :param message: The incoming callback query or message containing user input.
    :type message: CallbackQuery | Message
    :param user: Schema representing the current user, including their language settings.
    :type user: UserSchema
    :param state: Finite State Machine (FSM) context to manage user interactions.
    :type state: FSMContext
    :param keyboard_generator: Utility for generating dynamic or static keyboards based on configuration data.
    :type keyboard_generator: KeyboardGenerator
    """
    if isinstance(message, CallbackQuery):
        message = message.message
        message_id = message.message_id
    else:
        message_id = await state.get_value("message_id", message.message_id)
    await state.clear()

    text = localize_text_to_message(text_in_yaml="message_to_main_menu", lang=user.language_code)

    if user.is_admin:
        kb_key = "main_menu_for_admin_keyboard"
    else:
        kb_key = "main_menu_keyboard"
    keyboard = await keyboard_generator.generate_static_keyboard(kb_key=kb_key, lang=user.language_code)

    await send_message(
        chat_id=message.chat.id,
        message_id=message_id,
        text=text,
        reply_markup=keyboard,
        del_prev=True,
    )
