from src.core.settings import Configuration

logger = Configuration.logger.get_logger(name=__name__)


def create_allowed_instance_project_dict() -> dict:
    """
    Creates a dictionary for select instance from allowed instances in project.

    :returns: A dictionary representing the inline keyboard with available language options.
    :rtype: dict
    """
    allowed_languages = Configuration.settings.ALLOWED_LANGUAGES

    logger.info(f"allowed_languages: {allowed_languages}")
    result = {
        "keyboard_type": "inline",
        "row_width": [1, 1, 1, 1, 1],
        "fixed_top": [
            {"text": " ", "type": "callback", "data": "noop"},
            {"text": "Instance project menu", "type": "callback", "data": "noop"},
            # тут будет вызов метода, который будет по common_action_type брать название меню
            {"text": " ", "type": "callback", "data": "noop"},
        ],
        "button": [],
        "fixed_bottom": [
            {"text": "Back to menu", "type": "callback", "data": "{previous_callback}"},
            {"text": "Add instance", "type": "callback", "data": "prj:menu:ed:{id}:inst:add"},
        ],
    }
    # TODO: нужно будет здесь прописать логику как из бд брать
    # for instance in list_instances:
    #     text = instance_name
    #     logger.info(f"callback_data: {callback_data}")
    #     callback_str = ...

    dict_instances = {
        "Первый инст": "prj:menu:ed:{id}:inst:ed:1",
        "Второй инст": "prj:menu:ed:{id}:inst:ed:2",
        "Третий инст": "prj:menu:ed:{id}:inst:ed:3",
    }
    for key, value in dict_instances.items():
        text = key
        callback_str = value
        result["button"].append({"text": text, "type": "callback", "data": callback_str})
    return result
