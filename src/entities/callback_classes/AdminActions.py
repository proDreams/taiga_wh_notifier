from aiogram.filters.callback_data import CallbackData

from src.entities.enums.admin_action_type_enum import AdminActionTypeEnum


class AdminType(CallbackData, prefix="admin"):
    action_type: AdminActionTypeEnum


class SelectAdmin(AdminType, prefix="admin"):
    id: str = "0"


class ConfirmAdminAction(SelectAdmin, prefix="admin"):
    confirmed_action: str = "true"
