from pathlib import Path

import yaml
import yaml_include


def process_references(data) -> None:
    """
    Process references in the given data dictionary.

    :param data: The input data dictionary containing various sections.
    :type data: dict
    """
    if "buttons" not in data:
        return
    buttons = data["buttons"]

    for section, section_data in data.items():
        if section != "buttons" and isinstance(section_data, dict):
            buttons_list = section_data.get("buttons_list")
            if buttons_list:
                for i, row in enumerate(buttons_list):
                    for j, item in enumerate(row):
                        if isinstance(item, dict) and "ref" in item:
                            ref = item["ref"]
                            if ref in buttons:
                                button_def = buttons[ref].copy()
                                button_def.update({k: v for k, v in item.items() if k != "ref"})
                                buttons_list[i][j] = button_def
    data.pop("buttons")


def generate_strings_dict(path: str) -> dict[str, dict | list | str]:
    """
    Parses and processes YAML files in a given directory to extract string data.

    :param path: Path to the directory containing YAML files.
    :type path: str
    :returns: A dictionary where keys are file names (without extensions) and values are the parsed data from the YAML files.
    :rtype: dict[str, dict | list | str]
    """
    yaml.add_constructor("!include", yaml_include.Constructor(base_dir=path))
    strings_dict = {}

    for file_path in Path(path).glob("*.yaml"):
        with open(file_path, encoding="utf-8") as f:
            data = yaml.full_load(f)
            strings_dict[file_path.stem] = data
            process_references(data)

    return strings_dict
