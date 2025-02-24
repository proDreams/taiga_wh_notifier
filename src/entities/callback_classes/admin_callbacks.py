from aiogram.filters.callback_data import CallbackData

from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum, AdminMenuEnum


class AdminMenu(CallbackData, prefix="adm"):
    admin_menu: AdminMenuEnum


class AdminType(AdminMenu, prefix="adm"):
    action_type: AdminActionTypeEnum


class SelectAdmin(AdminType, prefix="adm"):
    admin_id: str = "0"


class ConfirmAdminAction(SelectAdmin, prefix="adm"):
    confirmed_action: str = "t"
