from src.logic.bot_logic.keyboards.keyboard_model import KeyboardGenerator


def create_allowed_admins_dict() -> dict:
    # TODO: заменить на реальную логику получения экземпляров
    dict_instances = [
        {"text": "Gnidina", "type": "callback", "data": "adm:menu:sel:1"},
    ]
    return KeyboardGenerator.get_dynamic_data(dict_instances)
