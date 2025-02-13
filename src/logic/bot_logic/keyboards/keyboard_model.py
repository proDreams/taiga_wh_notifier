from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.core.settings import Configuration


class KeyboardGenerator:
    def __init__(self):
        """
        Initialize the configuration settings for keyboard buttons and language data.

        This method sets up the `buttons` attribute using the string values retrieved from the Configuration class,
        specifically under the keys 'keyboards_buttons' and 'buttons'. It also initializes the `language_data`
        attribute by fetching the value associated with the key 'keyboards_language' and then accessing the
        'language' sub-key.

        :param: None - This method does not require any parameters.
        :return: None - This method does not return anything.
        """
        self.buttons = Configuration.strings.get("keyboards_buttons").get("buttons")
        self.language_data = Configuration.strings.get("keyboards_language").get("language")

    def create_static_keyboard(self, key: str, lang: str):
        """
        Creates a static keyboard based on provided configuration.

        :param key: The identifier for the keyboard to be created.
        :type key: str

        :param lang: The language code for the buttons in the keyboard.
        :type lang: str

        :returns: An InlineKeyboardMarkup or ReplyKeyboardMarkup object, depending on the keyboard type.
        :rtype: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]
        """
        data = Configuration.strings.get("keyboards_list").get(key)
        self._validate_keyboard_type(data.get("keyboard_type"))
        buttons = self.create_buttons(data.get("key"), data.get("keyboard_type"), lang=lang)
        rows = self._group_buttons(buttons, data.get("row_width"))

        if data.get("keyboard_type") == "inline":
            return InlineKeyboardMarkup(inline_keyboard=rows)
        elif data.get("keyboard_type") == "reply":
            return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

    @staticmethod
    def _validate_keyboard_type(keyboard_type: str):
        """
        Validates the type of a keyboard.

        :param keyboard_type: The type of the keyboard to validate.
        :type keyboard_type: str
        :raises ValueError: If the keyboard type is not 'inline' or 'reply'.
        """
        if keyboard_type not in ["inline", "reply"]:
            raise ValueError("Тип клавиатуры должен быть 'inline' или 'reply'.")

    def create_buttons(self, keys: list, keyboard_type: str, lang: str) -> list:
        """
        Creates a list of buttons based on the provided keys and keyboard type.

        :param keys: A list of button labels or other identifiers.
        :type keys: list
        :param keyboard_type: The type of keyboard to create buttons for, either "inline" or "reply".
        :type keyboard_type: str
        :param lang: The language in which the buttons should be created.
        :type lang: str
        :returns: A list of button objects created using the specified button creator function.
        :rtype: list
        :raises ValueError: If the provided keyboard_type is not one of the allowed values ("inline" or "reply").
        """
        button_creators = {
            "inline": self._create_inline_button,
            "reply": self._create_reply_button,
        }

        if keyboard_type not in button_creators:
            raise ValueError(f"Недопустимый тип клавиатуры: {keyboard_type}")

        return [button_creators[keyboard_type](key=key, lang=lang) for key in keys]

    def get_button_info(self, key: str):
        """
        Retrieves information about a button based on its key.

        :param key: The key of the button to retrieve information for.
        :type key: str
        :returns: Information about the button.
        :rtype: dict
        :raises ValueError: If a button with the given key is not found in the YAML configuration.
        """
        if key not in self.buttons:
            raise ValueError(f"Кнопка с ключом '{key}' не найдена в YAML.")
        return self.buttons[key]

    def _translate_button_text(self, key: str, lang: str) -> str:
        """
        Translates button text based on the provided key and language.

        :param key: The key corresponding to the text to be translated.
        :type key: str
        :param lang: The language code (e.g., 'en' for English, 'ru' for Russian) in which the text should be translated.
        :type lang: str
        :returns: The translated button text or the original key if no translation is available.
        :rtype: str
        """
        translated_text = self.language_data
        return translated_text.get(lang, {}).get(key, key)

    def _create_inline_button(self, key: str, lang: str) -> InlineKeyboardButton:
        """
        Creates an inline button for an InlineKeyboard markup.

        :param key: A unique identifier for the button.
        :type key: str
        :param lang: Language code for text translation.
        :type lang: str
        :returns: An InlineKeyboardButton object with translated text and specified attributes (url or callback_data).
        :rtype: InlineKeyboardButton
        :raises ValueError: If 'text' parameter is missing in button_info.
        :raises ValueError: If neither 'url' nor 'callback_data' is provided in button_info.
        """
        button_info = self.get_button_info(key)

        if not button_info.get("text"):
            raise ValueError(f"Кнопка '{key}': отсутствует обязательный параметр 'text'")

        if not ("url" in button_info or "callback_data" in button_info):
            raise ValueError(f"Кнопка '{key}': требуется 'url' или 'callback_data'")
        translated_text = self._translate_button_text(button_info.get("text"), lang=lang)

        return InlineKeyboardButton(
            text=translated_text, url=button_info.get("url"), callback_data=button_info.get("callback_data")
        )

    def _create_reply_button(self, key: str, lang: str) -> KeyboardButton:
        """
        Creates a reply button with translated text.

        :param key: The identifier for the button.
        :type key: str
        :param lang: The language code to translate the button text into.
        :type lang: str
        :returns: A KeyboardButton instance with the translated text.
        :rtype: KeyboardButton
        """
        button_info = self.get_button_info(key)
        translated_text = self._translate_button_text(button_info.get("text"), lang=lang)
        return KeyboardButton(text=translated_text)

    @staticmethod
    def _group_buttons(buttons: list, row_width: int) -> list:
        """
        Groups a list of buttons into rows based on the specified row width.

        :param buttons: List of button objects to be grouped.
        :type buttons: list
        :param row_width: Maximum number of buttons per row.
        :type row_width: int
        :returns: A list of lists, where each sublist represents a row of buttons.
        :rtype: list
        """
        grouped_buttons = []

        for start_index in range(0, len(buttons), row_width):
            end_index = start_index + row_width
            current_row = buttons[start_index:end_index]
            grouped_buttons.append(current_row)

        return grouped_buttons
