from aiogram.filters.callback_data import CallbackData

from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum


class AdminMenuData(CallbackData, prefix="adm"):
    page: int = 0


class AdminManageData(CallbackData, prefix="admin"):
    pass


class AddAdminData(CallbackData, prefix="add_admin"):
    pass


class AdminType(AdminMenuData, prefix="adm"):
    action_type: AdminActionTypeEnum


class SelectAdmin(AdminType, prefix="adm"):
    admin_id: str = "0"


class ConfirmAdminAction(SelectAdmin, prefix="adm"):
    confirmed_action: str = "t"
