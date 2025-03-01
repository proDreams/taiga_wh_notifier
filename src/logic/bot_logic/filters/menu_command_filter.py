from aiogram.filters import Filter
from aiogram.types import Message

from src.core.settings import get_settings
from src.utils.text_utils import localize_text_to_button


class MenuCommandFilter(Filter):
    """
    Filter to determine if a message text matches any of the localized command variants.
    """

    async def __call__(self, message: Message) -> bool:
        command_variants = [
            localize_text_to_button(text_in_yaml="get_main_menu", lang=lang)
            for lang in get_settings().ALLOWED_LANGUAGES
        ]
        return message.text in command_variants
