from aiogram.filters.callback_data import CallbackData

from src.entities.enums.edit_action_type_enum import EditActionTypeEnum


class ProjectType(CallbackData, prefix="project"):
    action_type: EditActionTypeEnum


class EditProject(ProjectType, prefix="project"):
    id: str = "0"


class ConfirmAction(EditProject, prefix="project"):
    confirmed_action: str = "true"
