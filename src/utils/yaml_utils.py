from pathlib import Path

import yaml


def get_strings() -> dict[str, str | dict[str, str | list]]:
    """
    Функция чтения всех YAML-файлов в директории strings и возврате единого словаря.

    :return: Словарь с содержимым YAML-файлов.
    """
    strings_dict = {}
    for path in Path("strings").glob("*.yaml"):
        with open(path, encoding="utf-8") as f:
            strings_dict.update({path.stem: dict(yaml.safe_load(f))})

    return strings_dict
