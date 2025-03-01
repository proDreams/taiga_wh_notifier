from aiogram import types
from aiogram.fsm.context import FSMContext

from src.core.settings import get_logger

logger = get_logger(name=__name__)


async def get_info_for_state(callback: types.CallbackQuery, state: FSMContext) -> str:
    """
    Retrieves the previous callback data from an FSMContext and updates it with the current callback data.

    :param callback: The CallbackQuery object containing the current callback information.
    :type callback: CallbackQuery

    :param state: The FSMContext object to retrieve and update data from.
    :type state: FSMContext

    :return: The previous callback data that was stored in the FSMContext.
    :rtype: str
    """
    data = await state.get_data()
    default_previous = "menu"
    callback_history = data.get("callback_history", {})

    current_callback = data.get("current_callback")

    if current_callback is None:
        callback_history[callback.data] = default_previous
        previous_callback = default_previous
    else:
        if callback.data not in callback_history:
            callback_history[callback.data] = current_callback

        previous_callback = callback_history[callback.data]

    data["current_callback"] = callback.data

    data["callback_history"] = callback_history
    await state.set_data(data)

    logger.info(f"callback.data={callback.data}")
    logger.info(f"previous_callback={previous_callback}")
    logger.info(f"callback_history={callback_history}")

    return previous_callback
