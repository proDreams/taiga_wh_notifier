from aiogram.fsm.state import State, StatesGroup


class ShareUsersSteps(StatesGroup):
    WAIT_USERS = State()
