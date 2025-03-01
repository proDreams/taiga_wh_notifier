from aiogram.filters.callback_data import CallbackData


class AdminMenuData(CallbackData, prefix="admin_menu"):
    """
    Represents the data structure for admin menu navigation.

    :ivar page: The current page number in the admin menu.
    :type page: int
    """

    page: int = 0


class AdminManageData(CallbackData, prefix="admin_data"):
    """
    Class for managing administrator-related data through a callback system.

    :ivar id: Unique identifier for the administrator data.
    :type id: str
    """

    id: str


class AdminRemoveData(AdminManageData, prefix="admin_remove"):
    """
    Class for removing admin.
    """

    pass


class AdminRemoveConfirmData(AdminManageData, prefix="admin_remove_confirm"):
    """
    Represents data for confirming an admin removal operation.
    """

    pass


class AdminAddData(CallbackData, prefix="add_admin"):
    """
    Class for adding an admin.
    """

    pass
