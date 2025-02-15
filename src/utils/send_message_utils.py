from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InputFile, Message, ReplyKeyboardMarkup

from src.core.Base.exceptions import BotBlocked
from src.core.settings import Configuration

logger = Configuration.logger.get_logger(name=__name__)


async def try_delete(chat_id: int, message_id: int) -> None:
    try:
        await Configuration.bot.delete_message(chat_id, message_id)
    except TelegramBadRequest as e:
        logger.warning(e.message)
    except TelegramForbiddenError:
        message = f"The bot is blocked by user: {chat_id}"
        logger.warning(message)
        raise BotBlocked(message=message)


async def send_message(
    chat_id: int,
    text: str,
    message_id: int = None,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup = None,
    try_to_edit: bool = False,
    del_prev: bool = False,
    **kwargs,
) -> Message | None:
    if try_to_edit:
        try:
            return await Configuration.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
                **kwargs,
            )
        except TelegramBadRequest as e:
            logger.warning(e.message)
            del_prev = True
        except TelegramForbiddenError:
            message = f"The bot is blocked by user: {chat_id}"
            logger.warning(message)
            return None

    if del_prev:
        try:
            await try_delete(chat_id=chat_id, message_id=message_id)
        except TelegramForbiddenError:
            return None

    try:
        return await Configuration.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, **kwargs)
    except TelegramForbiddenError:
        logger.warning(f"The bot is blocked by user: {chat_id}.")


async def send_photo(
    chat_id: int,
    photo: InputFile | str,
    message_id: int = None,
    caption: str = None,
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup = None,
    del_prev: bool = False,
) -> Message | None:
    if del_prev:
        try:
            await try_delete(chat_id=chat_id, message_id=message_id)
        except TelegramForbiddenError:
            return None

    try:
        return await Configuration.bot.send_photo(
            chat_id=chat_id, photo=photo, caption=caption, reply_markup=reply_markup
        )
    except TelegramForbiddenError:
        logger.warning(f"The bot is blocked by user: {chat_id}.")
