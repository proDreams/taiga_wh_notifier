from src.core.settings import Configuration
from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator

logger = Configuration.logger.get_logger(name=__name__)


def create_allowed_projects_dict() -> dict:
    # TODO: заменить на реальную логику получения проектов
    dict_projects = [{"text": "Test project", "type": "callback", "data": "prj:menu:ed:1"}]
    return KeyboardGenerator.get_dynamic_data(dict_projects)


def create_allowed_instances_project_dict() -> dict:
    # TODO: заменить на реальную логику получения экземпляров
    dict_instances = {
        "Первый инст": "prj:menu:ed:{id}:inst:ed:1",
        "Второй инст": "prj:menu:ed:{id}:inst:ed:2",
        "Третий инст": "prj:menu:ed:{id}:inst:ed:3",
    }
    return KeyboardGenerator.get_dynamic_data(dict_instances)
