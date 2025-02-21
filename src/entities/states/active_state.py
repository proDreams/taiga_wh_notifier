from aiogram.fsm.state import State, StatesGroup


class SingleState(StatesGroup):
    active = State()
