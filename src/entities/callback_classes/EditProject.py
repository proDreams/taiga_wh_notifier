from aiogram.filters.callback_data import CallbackData

from src.entities.enums.edit_action_type_enum import (
    EditActionTypeEnum,
    EditTargetPathEnum,
)
from src.entities.enums.event_enums import EventTypeEnum


class ProjectType(CallbackData, prefix="project"):
    action_type: EditActionTypeEnum


class EditProject(ProjectType, prefix="project"):
    id: str = "0"


class ConfirmAction(EditProject, prefix="project"):
    confirmed_action: str = "true"


class EditProjectFAT(EditProject, prefix="project"):
    fat_event_type: EventTypeEnum


class ConfirmActionFAT(EditProjectFAT, prefix="project"):
    confirmed_event: str = "true"


class EditTargetPath(EditProjectFAT, prefix="project"):
    target_action_type: EditTargetPathEnum


class ConfirmEditTargetPath(EditTargetPath, prefix="project"):
    confirmed_edit_target: str = "true"
