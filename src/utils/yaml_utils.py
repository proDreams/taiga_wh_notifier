from pathlib import Path

import yaml


def get_strings(path: str) -> dict[str, dict | list | str]:
    """
    Reads all YAML files in the specified directory and returns a dictionary of strings.

    :param path: Path to the directory containing YAML files.
    :type path: str
    :returns: A dictionary where each key is the base name of a YAML file and the value is a dictionary loaded from that file.
    :rtype: dict[str, dict | list | str]
    """
    strings_dict = {}
    for path in Path(path).glob("*.yaml"):
        with open(path, encoding="utf-8") as f:
            strings_dict.update({path.stem: dict(yaml.safe_load(f))})

    return strings_dict
