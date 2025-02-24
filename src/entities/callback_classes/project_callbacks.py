from aiogram.filters.callback_data import CallbackData

from src.entities.enums.edit_action_type_enum import (
    BaseProjectMenuEnum,
    ProjectInstanceActionEnum,
    ProjectsCommonMenuEnum,
    ProjectSelectedInstanceActionEnum,
    ProjectSelectedMenuEnum,
    ProjectSelectedTargetPathActionEnum,
    ProjectSelectedTargetPathEnum,
)
from src.entities.enums.event_enums import EventTypeEnum


class BaseProjectsMenu(CallbackData, prefix="prj"):
    """
    Главное меню проектов menu = `menu`

    Callback example: `prj:menu`
    """

    menu: BaseProjectMenuEnum


class ProjectsCommonMenu(BaseProjectsMenu, prefix="prj"):
    """
    Доступные действия для меню "Проекты":
        - добавить: {"ADD": "add"}
        - редактировать: {"EDIT": "ed"}

    Callback example:
        - добавить: `prj:menu:add`
        - редактировать: `prj:menu:ed`
    """

    common_action_type: ProjectsCommonMenuEnum


class ProjectID(ProjectsCommonMenu, prefix="prj"):
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


class ProjectSelectedMenu(ProjectID, prefix="prj"):
    """
    Доступные действия для выбранного "Проекта":
        - изменить имя: {"EDIT_NAME": "ed_n"}
        - редактировать экземпляры (инстансы): {"EDIT_INSTANCE": "inst"}
        - удалить: {"REMOVE": "rm"}

    Callback example:
        - `prj:menu:ed:{id}:ed_n`
        - `prj:menu:ed:{id}:inst`
        - `prj:menu:ed:{id}:rm`
    """

    selected_action_type: ProjectSelectedMenuEnum


class ConfirmAction(ProjectSelectedMenu, prefix="prj"):
    """
    Подтверждение действия для выбранного проекта из меню `ProjectSelectedMenu`:
        - подтверждение: {"confirmed_action": "t"}

    Callback example:
        - `prj:menu:ed:{id}:ed_n:t`
        - `prj:menu:ed:{id}:rm:t`
    """

    confirmed_action: str = "t"


class ProjectInstanceAction(ProjectSelectedMenu, prefix="prj"):
    """
    Доступные действия с экземплярами выбранного "Проекта":
        - добавить экземпляр: {"ADD": "add"}
        - редактировать экземпляр (инстанс): {"EDIT": "ed"}

    Callback example:
        - `prj:menu:ed:{id}:inst:add`
        - `prj:menu:ed:{id}:inst:ed`
    """

    instance_action: ProjectInstanceActionEnum


class ProjectInstanceID(ProjectInstanceAction, prefix="prj"):
    """
    Идентификатор выбранного экземпляра (инстанса) проекта :
        - идентификатор: {"id": str}

    Callback example:
        - `prj:menu:ed:{id}:inst:ed:{inst_id}`
    """

    inst_id: str


class ProjectInstanceActionConfirm(ProjectInstanceID, prefix="prj"):
    """
    Подтверждение действия с экземпляром выбранного проекта:
        - подтверждение: {"confirmed_instance_action": "t"}

    Callback example:
        - `prj:menu:ed:{id}:inst:add:t`
    """

    confirmed_instance_action: str = "t"


class ProjectSelectedInstanceAction(ProjectInstanceID, prefix="prj"):
    """
    Доступные действия с выбранным экземпляром "Проекта":
        - редактировать отслеживаемы действия экземпляра (инстанса): {"EDIT_FOLLOWING_ACTION_TYPE": "fat"}
        - редактировать целевой путь экземпляра (инстанса): {"EDIT_TARGET_PATH": "tr_pth"}
        - удалить экземпляр (инстанс): {"REMOVE": "rm"}

    Callback example:
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:fat`
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:tr_pth
        - `prj:menu:ed:{id}:inst:ed:{inst_id}:rm`
    """

    selected_instance_action: ProjectSelectedInstanceActionEnum


class ProjectEventFAT(ProjectSelectedInstanceAction, prefix="prj"):
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


class ConfirmActionFAT(ProjectEventFAT, prefix="prj"):
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


class ProjectTargetPath(ProjectSelectedInstanceAction, prefix="prj"):
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
