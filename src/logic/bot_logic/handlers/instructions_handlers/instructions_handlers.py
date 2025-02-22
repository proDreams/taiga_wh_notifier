from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.core.settings import Configuration
from src.entities.callback_classes.instruction_callbacks import Instructions
from src.entities.schemas.user_data.user_schemas import UserSchema
from src.entities.states.active_state import SingleState
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.utils.send_message_utils import send_message
from src.utils.state_utils import get_info_for_state
from src.utils.text_utils import localize_text_to_message

logger = Configuration.logger.get_logger(name=__name__)

instructions_router = Router()


@instructions_router.callback_query(Instructions.filter(), StateFilter(SingleState.active))
async def instructions_menu_handler(
    callback: CallbackQuery,
    user: UserSchema,
    state: FSMContext,
    keyboard: KeyboardGenerator = KeyboardGenerator(),
) -> None:
    """
    Handles the instructions menu callback query.

    :param callback: The callback query that triggered the handler.
    :type callback: CallbackQuery

    :param user: The user that triggered the handler.
    :type user: UserSchema

    :param state: The state that triggered the handler.
    :type state: FSMContext

    :param keyboard: A generator for creating keyboards.
    :type keyboard: KeyboardGenerator
    """

    await send_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=localize_text_to_message(text_in_yaml="message_to_instructions", lang=user.language_code),
        reply_markup=keyboard.create_static_keyboard(
            key="instructions_keyboard",
            lang=user.language_code,
            placeholder={"previous_callback": await get_info_for_state(callback=callback, state=state)},
        ),
        try_to_edit=True,
    )
