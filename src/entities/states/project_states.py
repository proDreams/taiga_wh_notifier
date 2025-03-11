from aiogram.fsm.state import State, StatesGroup


class ProjectNameState(StatesGroup):
    """
    Class for managing the input of project name in a states-based system.

    :ivar WAIT_NAME: State indicating that the system is waiting for project name.
    :type WAIT_NAME: State
    """

    WAIT_NAME = State()


class ProjectEditNameState(StatesGroup):
    WAIT_NAME = State()


class InstanceNameState(StatesGroup):
    WAIT_INSTANCE_NAME = State()


class InstanceEditNameState(StatesGroup):
    WAIT_INSTANCE_NAME = State()


class InstanceEditChatIDState(StatesGroup):
    WAIT_INSTANCE_CHAT_ID = State()


class InstanceEditThreadIDState(StatesGroup):
    WAIT_INSTANCE_THREAD_ID = State()
