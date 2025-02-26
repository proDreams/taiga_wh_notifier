from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.settings import Configuration
from src.entities.callback_classes.menu_callbacks import MenuData
from src.entities.enums.handlers_enum import CommandsEnum
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.text_utils import localize_text_to_message

logger = Configuration.logger.get_logger(name=__name__)

main_router = Router()


@main_router.message(Command(commands=[CommandsEnum.START]))
async def start_handler(
    message: Message, state: FSMContext, user: UserSchema, keyboard_generator: KeyboardGenerator
) -> None:
    await state.clear()

    await send_message(
        chat_id=message.chat.id,
        text=localize_text_to_message(text_in_yaml="message_to_start", lang=user.language_code),
        reply_markup=await keyboard_generator.generate_static_keyboard(
            kb_key="start_keyboard", lang=user.language_code
        ),
    )


@main_router.callback_query(MenuData.filter())
async def main_menu_handler(
    callback: CallbackQuery, user: UserSchema, state: FSMContext, keyboard_generator: KeyboardGenerator
) -> None:
    await state.clear()

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_main_menu", lang=user.language_code),
        reply_markup=await keyboard_generator.generate_static_keyboard(
            kb_key="main_menu_keyboard", lang=user.language_code
        ),
        try_to_edit=True,
    )
