from aiogram.filters.callback_data import CallbackData

from src.entities.enums.edit_action_type_enum import (
    ProjectSelectedTargetPathActionEnum,
    ProjectSelectedTargetPathEnum,
)
from src.entities.enums.event_enums import EventTypeEnum


class ProjectMenuData(CallbackData, prefix="project"):
    page: int = 0


class AddProject(CallbackData, prefix="prj_menu_add"):
    pass


class ProjectID(CallbackData, prefix="project_id"):
    """
    Выбор конкретного "Проекта":
        - идентификатор {"id": str}

    Callback example:
        - `prj:menu:ed:{id}`
    """

    id: str = "0"


class ProjectAddedConfirm(ProjectID, prefix="prj"):
    """
    Подтверждение создания "Проекта":
        - подтверждение: {"confirmed_action": "t"}

    Callback example:
        - `prj:menu:add:{id}:t``
    """

    confirmed_add: str = "t"


class RemoveProject(ProjectID, prefix="project_remove"):
    pass


class ProjectEditName(ProjectID, prefix="project_edit_name"):
    pass


class ProjectEditInstance(ProjectID, prefix="project_edit_instance"):
    pass


class ConfirmRemoveProject(RemoveProject, prefix="confirm_remove_project"):
    pass


class ConfirmProjectEditName(ProjectEditName, prefix="confirm_project_edit_name"):
    pass


class EditProjectInstance(ProjectID, ProjectMenuData, prefix="edit_instance"):
    pass


class AddProjectInstance(ProjectID, prefix="add_project_instance"):
    pass


class ConfirmAddInstance(AddProjectInstance, prefix="confirm_add_instance"):
    pass


class ProjectInstanceID(CallbackData, prefix="project_instance"):
    inst_id: str = "0"


class EditInstanceFAT(ProjectInstanceID, prefix="instance_edit_fat"):
    pass


class EditInstanceTargetPath(ProjectInstanceID, prefix="instance_edit_target_path"):
    pass


class RemoveInstance(ProjectInstanceID, prefix="remove_instance"):
    pass


class ConfirmRemoveInstance(RemoveInstance, prefix="confirm_remove_instance"):
    pass


class ChangeInstanceName(ProjectInstanceID, prefix="change_instance_name"):
    pass


class ConfirmChangeInstanceName(ProjectInstanceID, prefix="confirm_change_instance_name"):
    pass


class ProjectEventFAT(ProjectInstanceID, prefix="instance_edit_fat"):
    """
    Доступные типы событий для отслеживания для выбранного экземпляра "Проекта":
        - эпик: {EPIC = "epic"}
        - спринт: {MILESTONE = "milestone"}
        - пользовательская история: {USERSTORY = "userstory"}
        - задача: {TASK = "task"}
        - запрос: {ISSUE = "issue"}
        - вики: {WIKIPAGE = "wikipage"}
        - тест: {TEST = "test"}

    Callback example:
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:epic`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:milestone`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:userstory`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:task`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:issue`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:wikipage`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:test`
    """

    fat_event_type: EventTypeEnum


class ConfirmActionFAT(ProjectEventFAT, prefix="confirm_instance_edit_fat"):
    """
    Подтверждение для отслеживания выбранного типа событий в конкретном экземпляре проекта:
        - подтверждение: {"confirmed_event": "t"}

    Callback example:
        Universal:
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:{fat_event_type}:t`
        Specific:
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:epic:t`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:milestone:t`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:userstory:t`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:task:t`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:issue:t`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:wikipage:t`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat:test:t`
    """

    confirmed_event: str = "t"


class ProjectTargetPath(ProjectInstanceID, prefix="edit_instance_target_path"):
    """
    Доступные типы источников для отправки уведомлений для выбранного экземпляра "Проекта":
        - изменить Chat ID: {EDIT_CHAT_ID = "ch_id"}
        - изменить Thread ID: {EDIT_THREAD_ID = "thr_id"}

    Callback example:
        Universal:
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:thr_id`
            - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:сh_id`
        Specific:
            -`prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:{target_action_type}`
    """

    target_action_type: ProjectSelectedTargetPathEnum


class ActionEditTargetPath(ProjectTargetPath, prefix="prj"):
    """
    Доступные действия с типами источников в рамках экземпляра выбранного "Проекта":
        - изменим источников: {"CHANGE": "ch"}
        - удалить источник: {"REMOVE": "rm"}

    Callback example:
        Universal:
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:{target_action_type}:ch`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:{target_action_type}:rm`
        Specific:
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:thr_id:ch`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:ch_id:ch`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:thr_id:rm`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:ch_id:rm`
    """

    action_target_edit: ProjectSelectedTargetPathActionEnum


class ConfirmActionEditTargetPath(ActionEditTargetPath, prefix="prj"):
    """
    Подтверждение для изменения информации в выбранном источнике для отправки уведомлений в рамках конкретного
    экземпляра проекта:
        - подтверждение: {"confirmed_action_edit_target": "t"}

    Callback example:
        Universal:
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:{target_action_type}:{action_target_edit}:t`
        Specific:
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:thr_id:ch:t`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:ch_id:ch:t`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:thr_id:rm:t`
          - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth:ch_id:rm:t`
    """

    confirmed_action_edit_target: str = "t"
