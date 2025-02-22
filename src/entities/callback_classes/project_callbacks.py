from aiogram.filters.callback_data import CallbackData

from src.entities.enums.edit_action_type_enum import (
    EditActionTypeEnum,
    EditTargetPathEnum,
    EventTargetPathActionEnum,
)
from src.entities.enums.event_enums import EventTypeEnum


class ProjectType(CallbackData, prefix="prj"):
    action_type: EditActionTypeEnum


class EditProject(ProjectType, prefix="prj"):
    id: str = "0"


class ConfirmAction(EditProject, prefix="prj"):
    confirmed_action: str = "t"


class EditProjectFAT(EditProject, prefix="prj"):
    fat_event_type: EventTypeEnum


class ConfirmActionFAT(EditProjectFAT, prefix="prj"):
    confirmed_event: str = "t"


class EditTargetPath(EditProjectFAT, prefix="prj"):
    target_action_type: EditTargetPathEnum


class ConfirmEditTargetPath(EditTargetPath, prefix="prj"):
    confirmed_edit_target: str = "t"


class ActionEditTargetPath(EditTargetPath, prefix="prj"):
    action_target_edit: EventTargetPathActionEnum


class ConfirmActionEditTargetPath(ActionEditTargetPath, prefix="prj"):
    confirmed_action_edit_target: str = "t"
