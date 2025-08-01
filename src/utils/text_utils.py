from typing import Any

import nh3

from src.core.settings import Configuration, get_settings, get_strings
from src.entities.named_tuples.utils_tuples import AdminStrTuple
from src.entities.schemas.user_data.user_schemas import UserCreateSchema


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


def localize_text_to_message(text_in_yaml: str, lang: str, **kwargs):
    """
    Translates text from a YAML configuration to a message based on the specified language.

    :param text_in_yaml: The key used to retrieve the text from the 'messages_text' dictionary.
    :type text_in_yaml: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :param kwargs: Key-value pairs to format into the YAML text.
    :type kwargs: str or bool
    :returns: Translated text or default if not found.
    :rtype: str
    """
    return format_text_with_kwargs(
        text_in_yaml=get_strings().get("messages_text").get(lang).get(text_in_yaml),
        **kwargs,
    )


def localize_text_to_button(text_in_yaml: str, lang: str, **kwargs):
    """
    Translates text from a YAML configuration to a message based on the specified language.

    :param text_in_yaml: The key used to retrieve the text from the 'messages_text' dictionary.
    :type text_in_yaml: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :param kwargs: Key-value pairs to format into the YAML text.
    :type kwargs: str
    :returns: Translated text or default if not found.
    :rtype: str
    """
    return format_text_with_kwargs(
        text_in_yaml=get_strings().get("keyboard_text").get(lang).get(text_in_yaml),
        **kwargs,
    )


def get_webhook_notification_text(text_in_yaml: str, lang: str, **kwargs):
    """
    Translates text from a YAML configuration to a message based on the specified language.

    :param text_in_yaml: The key used to retrieve the text from the 'webhook_notifications' dictionary.
    :type text_in_yaml: str
    :param lang: The language code (key) to select the appropriate translation.
    :type lang: str
    :param kwargs: Key-value pairs to format into the YAML text.
    :type kwargs: str
    :returns: Translated text or default if not found.
    :rtype: str
    """
    return format_text_with_kwargs(
        text_in_yaml=get_strings().get("webhook_notifications").get(lang).get(text_in_yaml),
        **kwargs,
    )


def get_service_text(text_in_yaml: str, **kwargs) -> str:
    """
    Retrieves and formats a service-specific text based on the provided YAML key.

    :param text_in_yaml: The key to look up in the YAML strings dictionary.
    :type text_in_yaml: str
    **kwargs: Additional keyword arguments to be used for formatting the retrieved string.
    :return: The formatted service text as a string.
    :rtype: str
    """
    return format_text_with_kwargs(get_strings().get("service_text").get(text_in_yaml), **kwargs)


async def generate_admins_text(admins_list: list[UserCreateSchema]) -> AdminStrTuple:
    """
    Generates a formatted text string containing information about admins and the bot link.

    :param admins_list: A list of UserCreateSchema objects representing administrators.
    :type admins_list: list[UserCreateSchema]
    :return: A tuple containing a formatted text string of admin details and the bot's URL.
    :rtype: tuple[str, str]
    """
    admin_str = "\n".join(
        [f"- <code>{admin.telegram_id}</code> <code>{admin.full_name}</code>" for admin in admins_list]
    )
    bot_obj = await Configuration.bot.me()
    bot_link = bot_obj.url

    return AdminStrTuple(admin_str=admin_str, bot_link=bot_link)


def get_untag_truncated_string(obj: Any) -> Any:
    """
    Remove tags and truncate the string if its length exceeds the specified value.

    :param obj: Object to process.
    :type obj: Any
    :returns: A string with removed tags, not exceeding the specified length,
    or the original object if it is not of string type.
    :rtype: Any
    """

    if not isinstance(obj, str):
        return obj

    allowed_tags: set[str] = {
        "b",
        "strong",
        "i",
        "em",
        "u",
        "ins",
        "s",
        "strike",
        "del",
        "span",
        "tg-spoiler",
        "a",
        "tg-emoji",
        "code",
        "pre",
        "blockquote",
    }

    allowed_attributes: dict[str, set[str]] = {
        "span": {"class"},
        "a": {"href"},
        "tg-emoji": {"emoji-id"},
        "code": {"class"},
    }

    untag_obj = nh3.clean(html=obj, tags=allowed_tags, attributes=allowed_attributes)

    maximum_text_length = get_settings().TRUNCATED_STRING_LENGTH

    if len(untag_obj) > maximum_text_length:
        return untag_obj[:maximum_text_length] + "..."
    return untag_obj


def get_blockquote_tagged_string(text_string: str) -> str:
    """
    Add 'blockquote' tags to the input text_string.

    :param text_string: Input text_string.
    :type text_string: str
    :returns: A string with added tags.
    :rtype: str
    """

    return f"<blockquote>{text_string}</blockquote>"
