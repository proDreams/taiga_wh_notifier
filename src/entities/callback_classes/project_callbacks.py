from aiogram.filters.callback_data import CallbackData


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
    instance_id: str = "0"


class EditInstanceFAT(ProjectInstanceID, prefix="instance_edit_fat"):
    pass


class RemoveInstance(ProjectInstanceID, prefix="remove_instance"):
    pass


class ConfirmRemoveInstance(RemoveInstance, prefix="confirm_remove_instance"):
    pass


class ChangeInstanceName(ProjectInstanceID, prefix="change_instance_name"):
    pass


class ConfirmChangeInstanceName(ProjectInstanceID, prefix="confirm_change_instance_name"):
    pass


class InstanceTargetPath(ProjectInstanceID, prefix="edit_instance_target_path"):
    """
    Доступные типы источников для отправки уведомлений для выбранного экземпляра "Проекта"
    """

    pass


class EditInstanceChatID(ProjectInstanceID, prefix="edit_instance_chat_id"):
    pass


class ConfirmEditInstanceChatID(ProjectInstanceID, prefix="confirm_edit_instance_chat_id"):
    pass


class EditInstanceThreadID(ProjectInstanceID, prefix="edit_instance_thread_id"):
    pass


class ConfirmEditInstanceThreadID(ProjectInstanceID, prefix="confirm_edit_instance_thread_id"):
    pass
