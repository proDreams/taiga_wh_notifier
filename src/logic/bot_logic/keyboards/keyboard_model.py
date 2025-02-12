from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class KeyboardGenerator:
    def __init__(self, buttons_data: dict, keyboard_type: str = "inline"):
        """
        Инициализация генератора клавиатур с загрузкой данных из YAML.
        :param buttons_data: Словарь с доступными кнопками из конфигурационного файла клавиатуры.
        :param keyboard_type: Тип клавиатуры ("inline" или "reply").
        """
        self.buttons = buttons_data
        self.keyboard_type = keyboard_type.lower()

    def create_keyboard(self, keys: list, keyboard_type: str = "inline", row_width: int = 1):
        """
        Создаёт клавиатуру на основе переданных ключей и типа клавиатуры.
        :param keys: Список ключей кнопок из YAML.
        :param keyboard_type: Тип клавиатуры ("inline" или "reply").
        :param row_width: Количество кнопок в ряду.
        :return: Объект InlineKeyboardMarkup или ReplyKeyboardMarkup.
        """
        self._validate_keyboard_type(keyboard_type)
        buttons = self.create_buttons(keys, keyboard_type)
        rows = self._group_buttons(buttons, row_width)

        if keyboard_type == "inline":
            return InlineKeyboardMarkup(inline_keyboard=rows)
        elif keyboard_type == "reply":
            return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

    @staticmethod
    def _validate_keyboard_type(keyboard_type: str):
        """
        Проверяет корректность типа клавиатуры.
        :param keyboard_type: Тип клавиатуры ("inline" или "reply").
        """
        if keyboard_type not in ["inline", "reply"]:
            raise ValueError("Тип клавиатуры должен быть 'inline' или 'reply'.")

    def create_buttons(self, keys: list, keyboard_type: str) -> list:
        """
        Создаёт список кнопок на основе переданных ключей и типа клавиатуры.

        Пример:
            keys = ["btn1", "btn2"]
            create_buttons(keys, "inline")
            -> [InlineKeyboardButton(...), ...]

        :param keys: Список ключей кнопок из YAML.
        :param keyboard_type: Тип клавиатуры ("inline" или "reply").
        :return: Список кнопок.
        :raises ValueError: Если тип клавиатуры неверен или отсутствуют обязательные поля.
        """
        button_creators = {"inline": self._create_inline_button, "reply": self._create_reply_button}

        if keyboard_type not in button_creators:
            raise ValueError(f"Недопустимый тип клавиатуры: {keyboard_type}")

        return [button_creators[keyboard_type](key) for key in keys]

    def get_button_info(self, key: str):
        """
        Получает информацию о кнопке из YAML по ключу.
        :param key: Ключ кнопки.
        :return: Словарь с информацией о кнопке.
        """
        if key not in self.buttons:
            raise ValueError(f"Кнопка с ключом '{key}' не найдена в YAML.")
        return self.buttons[key]

    def _create_inline_button(self, key: str) -> InlineKeyboardButton:
        """Создает Inline-кнопку с проверкой обязательных параметров."""
        button_info = self.get_button_info(key)

        if not button_info.get("text"):
            raise ValueError(f"Кнопка '{key}': отсутствует обязательный параметр 'text'")

        if not ("url" in button_info or "callback_data" in button_info):
            raise ValueError(f"Кнопка '{key}': требуется 'url' или 'callback_data'")

        return InlineKeyboardButton(
            text=button_info["text"], url=button_info.get("url"), callback_data=button_info.get("callback_data")
        )

    def _create_reply_button(self, key: str) -> KeyboardButton:
        """Создает KeyboardButton."""
        button_info = self.get_button_info(key)
        return KeyboardButton(text=button_info["text"])

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
