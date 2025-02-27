from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardMarkup, InputFile, Message, ReplyKeyboardMarkup

from src.core.Base.exceptions import BotBlocked
from src.core.settings import Configuration

logger = Configuration.logger.get_logger(name=__name__)


async def try_delete(chat_id: int, message_id: int) -> None:
    """
    Attempts to delete a message in a Telegram chat.

    :param chat_id: Unique identifier for the target chat.
    :type chat_id: int
    :param message_id: Unique identifier of the message to be deleted.
    :type message_id: int
    :raises BotBlocked: If the bot is blocked by the user.
    """
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
    reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None = None,
    try_to_edit: bool = False,
    del_prev: bool = False,
    **kwargs,
) -> Message | None:
    """
    Sends a message to a chat or edits an existing message.

    :param chat_id: Unique identifier for the target chat.
    :type chat_id: int
    :param text: Text of the message to be sent; can be empty (for sending only media, without a text).
    :type text: str
    :param message_id: Unique identifier of the message to edit.
    :type message_id: int or None
    :param reply_markup: Markup for replying to messages.
    :type reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | None
    :param try_to_edit: Whether to attempt editing an existing message if possible.
    :type try_to_edit: bool
    :param del_prev: Whether to delete the previous message before sending a new one.
    :type del_prev: bool
    :returns: The sent or edited message, or `None` if the bot is blocked or an error occurs.
    :rtype: Message or None
    :raises TelegramBadRequest: If the edit request fails with a bad request.
    :raises TelegramForbiddenError: If the bot is blocked by the user.
    """
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
    """
    Sends a photo to a specified chat.

    :param chat_id: Unique identifier for the target chat.
    :type chat_id: int
    :param photo: A file object or a string with the URL of the photo to send.
    :type photo: InputFile | str
    :param message_id: Unique identifier for the message to edit.
    :type message_id: int, optional
    :param caption: Optional caption to attach to the photo.
    :type caption: str, optional
    :param reply_markup: Additional interface options like keyboards or buttons.
    :type reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup, optional
    :param del_prev: Indicates whether to delete the previous message before sending a new one.
    :type del_prev: bool, optional
    :returns: The sent message object if successful, otherwise None.
    :rtype: Message | None
    :raises TelegramForbiddenError: If the bot does not have permission to send messages or edit the specified message.
    """
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
