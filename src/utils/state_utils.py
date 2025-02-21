from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


async def get_info_for_state(callback: CallbackQuery, state: FSMContext) -> str:
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
    previous_callback = data.get("previous_callback")
    await state.update_data(previous_callback=callback.data)
    return previous_callback
