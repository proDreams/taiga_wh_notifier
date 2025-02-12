from aiogram import F, Router
from aiogram.types import Message

from src.core.settings import Configuration
from src.logic.bot_logic.keyboards.keyboards_stash import started_keyboard

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message):
    """Запускает обработчик команды /start.

    Отвечает на команду /start и отправляет сообщение с реплай-клавиатурой.
    """
    await message.answer(
        Configuration.strings.get("messages_text").get("message_to_start"), reply_markup=started_keyboard
    )
