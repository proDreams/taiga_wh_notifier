from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import Configuration
from src.entities.callback_classes.pagination_callbacks import Pagination
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.text_utils import localize_text_to_message

logger = Configuration.logger.get_logger(name=__name__)

main_router = Router()


@main_router.message(F.text == "/start", StateFilter("*"))
async def start_handler(
    message: Message, state: FSMContext, user: UserSchema, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the '/start' command by sending a welcome message.

    :param message: The incoming message object containing the '/start' command.
    :param state: The incoming state object containing the '/start' command.
    :param user: The incoming user object containing the '/start' command.
    :param keyboard: The incoming keyboard object containing the '/start' command.
    :type message: Message
    """
    await state.clear()
    await send_message(
        chat_id=message.chat.id,
        text=localize_text_to_message(text_in_yaml="message_to_start", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang=user.language_code),
    )


@main_router.callback_query(F.data == "menu", StateFilter("*"))
async def main_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard: KeyboardGenerator = KeyboardGenerator()
) -> None:
    """
    Handles the main menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The incoming user object.
    :type user: UserSchema

    :param state: The incoming state object.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    await state.clear()
    await state.set_state(SingleState.active.state)
    await state.update_data(previous_callback=callback.data)
    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_main_menu", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(key="main_menu_keyboard", lang=user.language_code),
        try_to_edit=True,
    )


@main_router.callback_query(Pagination.filter())
async def paginate_keyboard(
    callback: CallbackQuery,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
    callback_data: Pagination = Pagination,
) -> None:
    page = callback_data.page
    key_in_storage = callback_data.key_in_storage

    example = keyboard.get_buttons_dict(key_in_storage=key_in_storage)
    logger.info(f"Keyboard example: {example}")
    await callback.message.edit_reply_markup(
        reply_markup=keyboard.create_dynamic_keyboard(
            buttons_dict=example,
            lang=user.language_code,
            keyboard_type=example.get("keyboard_type"),
            row_width=example.get("row_width"),
            key_header_title=example.get("header_title"),
            key_additional_action=example.get("additional_action"),
            key_in_storage=key_in_storage,
            page=page,
            placeholder=example.get("placeholder"),
        )
    )
    await callback.answer()
