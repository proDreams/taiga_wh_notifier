from aiogram import Router
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.Instructions import Instructions
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.text_utils import format_text_with_kwargs

logger = Configuration.logger.get_logger(name=__name__)

instructions_router = Router()


@instructions_router.callback_query(Instructions.filter())
async def instructions_menu_handler(
    callback: CallbackQuery,
    user: UserSchema,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the instructions menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """
    result_message = format_text_with_kwargs(
        text_in_yaml=Configuration.strings.get("messages_text").get("message_to_instructions")
    )

    await callback.message.edit_text(
        result_message, reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang=user.language_code)
    )
