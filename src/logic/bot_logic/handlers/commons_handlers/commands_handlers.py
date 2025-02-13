from aiogram import F, Router
from aiogram.types import Message

from src.core.settings import Configuration
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, keyboard: KeyboardGenerator = KeyboardGenerator()) -> None:
    """
    Handles the '/start' command by sending a welcome message.

    :param keyboard:
    :param message: The incoming message object containing the '/start' command.
    :type message: Message
    """
    await message.answer(
        Configuration.strings.get("messages_text").get("message_to_start"),
        reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
    )
