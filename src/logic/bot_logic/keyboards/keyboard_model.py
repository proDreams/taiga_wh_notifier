from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.core.settings import Configuration

# keyboards = KeyboardGenerator(
#     buttons_data=strings.get("keyboards_buttons").get("buttons"),
#     language_data=Configuration.strings.get("keyboards_language").get("language"),
# )


class KeyboardGenerator:
    def __init__(self):
        """
        Инициализация генератора клавиатур с загрузкой данных из YAML.
        """
        self.buttons = Configuration.strings.get("keyboards_buttons").get("buttons")
        self.language_data = Configuration.strings.get("keyboards_language").get("language")

    def create_static_keyboard(self, key: str, lang: str):
        """
        Создаёт клавиатуру на основе переданных ключей и типа клавиатуры.
        :param key: Список ключей кнопок из YAML.
        :param lang: Язык системы пользователя.
        :return: Объект InlineKeyboardMarkup или ReplyKeyboardMarkup.
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
        Проверяет корректность типа клавиатуры.
        :param keyboard_type: Тип клавиатуры ("inline" или "reply").
        """
        if keyboard_type not in ["inline", "reply"]:
            raise ValueError("Тип клавиатуры должен быть 'inline' или 'reply'.")

    def create_buttons(self, keys: list, keyboard_type: str, lang: str) -> list:
        """
        Создаёт список кнопок на основе переданных ключей и типа клавиатуры.

        Пример:
            keys = ["btn1", "btn2"]
            create_buttons(keys, "inline")
            -> [InlineKeyboardButton(...), ...]

        :param lang: Системный язык пользователя
        :param keys: Список ключей кнопок из YAML.
        :param keyboard_type: Тип клавиатуры ("inline" или "reply").
        :return: Список кнопок.
        :raises ValueError: Если тип клавиатуры неверен или отсутствуют обязательные поля.
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
        Получает информацию о кнопке из YAML по ключу.
        :param key: Ключ кнопки.
        :return: Словарь с информацией о кнопке.
        """
        if key not in self.buttons:
            raise ValueError(f"Кнопка с ключом '{key}' не найдена в YAML.")
        return self.buttons[key]

    def _translate_button_text(self, key: str, lang: str) -> str:
        translated_text = self.language_data
        return translated_text.get(lang, {}).get(key, key)

    def _create_inline_button(self, key: str, lang: str) -> InlineKeyboardButton:
        """Создает Inline-кнопку с проверкой обязательных параметров."""
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
        """Создает KeyboardButton."""
        button_info = self.get_button_info(key)
        translated_text = self._translate_button_text(button_info.get("text"), lang=lang)
        return KeyboardButton(text=translated_text)

    @staticmethod
    def _group_buttons(buttons: list, row_width: int) -> list:
        """
        Группирует кнопки в ряды.
        :param buttons: Список кнопок.
        :param row_width: Количество кнопок в ряду.
        :return: Список списков кнопок.
        """
        grouped_buttons = []

        for start_index in range(0, len(buttons), row_width):
            end_index = start_index + row_width
            current_row = buttons[start_index:end_index]
            grouped_buttons.append(current_row)

        return grouped_buttons
