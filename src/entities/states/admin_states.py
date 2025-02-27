from aiogram.fsm.state import State, StatesGroup


class ShareUsersSteps(StatesGroup):
    """
    Class for managing the sharing of users in a states-based system.

    :ivar WAIT_USERS: State indicating that the system is waiting for user information.
    :type WAIT_USERS: State
    """

    WAIT_USERS = State()
