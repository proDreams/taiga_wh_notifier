from aiogram.fsm.state import State, StatesGroup


class ProjectNameState(StatesGroup):
    """
    Class for managing the input of project name in a states-based system.

    :ivar WAIT_NAME: State indicating that the system is waiting for project name.
    :type WAIT_NAME: State
    """

    WAIT_NAME = State()
