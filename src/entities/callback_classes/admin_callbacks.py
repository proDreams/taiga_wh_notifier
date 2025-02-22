from aiogram.filters.callback_data import CallbackData

from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum


class AdminType(CallbackData, prefix="adm"):
    action_type: AdminActionTypeEnum


class SelectAdmin(AdminType, prefix="adm"):
    id: str = "0"


class ConfirmAdminAction(SelectAdmin, prefix="adm"):
    confirmed_action: str = "t"
