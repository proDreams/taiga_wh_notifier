from aiogram import F, Router
from aiogram.types import Message

from src.core.settings import Configuration
from src.logic.bot_logic.keyboards.keyboards_stash import started_keyboard

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    """
    Handles the '/start' command by sending a welcome message.

    :param message: The incoming message object containing the '/start' command.
    :type message: Message
    """
    await message.answer(
        Configuration.strings.get("messages_text").get("message_to_start"), reply_markup=started_keyboard
    )
