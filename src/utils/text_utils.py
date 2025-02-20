from src.core.settings import Configuration


def format_text_with_kwargs(text_in_yaml: str, **kwargs) -> str:
    """
    Formats the input YAML text with the provided keyword arguments.

    :param text_in_yaml: YAML formatted string to be formatted.
    :type text_in_yaml: str
    :param kwargs: Key-value pairs to format into the YAML text.
    :type kwargs: dict
    :returns: Formatted YAML string.
    :rtype: str
    :raises ValueError: If any key in kwargs is not found in the text_in_yaml.
    """
    return text_in_yaml.format(**kwargs)


def localize_text_to_message(text_in_yaml: str, lang: str):
    """
    Translates text from a YAML configuration to a message based on the specified language.

    :param text_in_yaml: The key used to retrieve the text from the 'messages_text' dictionary.
    :type text_in_yaml: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :returns: Translated text or default if not found.
    :rtype: str
    """
    return Configuration.strings.get("messages_text").get(lang).get(text_in_yaml)
