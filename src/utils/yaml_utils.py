from pathlib import Path

import yaml


def get_strings(path: str) -> dict[str, dict | list | str]:
    """
    Функция чтения всех YAML-файлов в директории strings и возврате единого словаря.

    :return: Словарь с содержимым YAML-файлов.
    """
    strings_dict = {}
    for path in Path(path).glob("*.yaml"):
        with open(path, encoding="utf-8") as f:
            strings_dict.update({path.stem: dict(yaml.safe_load(f))})

    return strings_dict
