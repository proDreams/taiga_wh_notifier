from aiogram.filters.callback_data import CallbackData

from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum


class AdminMenuData(CallbackData, prefix="admin_menu"):
    page: int = 0


class AdminManageData(CallbackData, prefix="admin_data"):
    id: str


class AdminRemoveData(AdminManageData, prefix="admin_remove"):
    pass


class AdminRemoveConfirmData(AdminManageData, prefix="admin_remove_confirm"):
    pass


class AdminAddData(CallbackData, prefix="add_admin"):
    pass


class AdminType(AdminMenuData, prefix="adm"):
    action_type: AdminActionTypeEnum


class SelectAdmin(AdminType, prefix="adm"):
    admin_id: str = "0"


class ConfirmAdminAction(SelectAdmin, prefix="adm"):
    confirmed_action: str = "t"
