from src.core.settings import get_logger
from src.entities.callback_classes.project_callbacks import SelectInstance
from src.entities.enums.edit_action_type_enum import ProjectsCommonMenuEnum
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator
from src.logic.services.project_service import ProjectService

logger = get_logger(name=__name__)


def create_allowed_projects_dict() -> dict:
    # TODO: заменить на реальную логику получения проектов
    dict_projects = [{"text": "Test project", "type": "callback", "data": "prj:menu:ed:1"}]
    return KeyboardGenerator.get_dynamic_data(dict_projects)


def create_allowed_instances_project_dict(project_id: str) -> dict:
    project = ProjectService().get_project(project_id=project_id)
    if project:
        instances = project.instances
    instance_buttons = []
    for inst in instances:
        text = (inst.name,)
        callback_str = SelectInstance(
            common_action_type=ProjectsCommonMenuEnum.ADD,
            id=project_id,
            instance_id=inst.id,
        ).pack()
        instance_buttons.append({"text": text, "type": "callback", "data": callback_str})
    return KeyboardGenerator.get_dynamic_data(instance_buttons)
