from math import ceil

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.core.settings import Configuration
from src.entities.callback_classes.Pagination import Pagination
from src.utils.text_utils import format_text_with_kwargs

logger = Configuration.logger.get_logger(name=__name__)


class KeyboardGenerator:
    BUTTONS_KEYBOARD_STORAGE = {}

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

    @classmethod
    def add_keyboard_to_storage(cls, key_in_storage: str, buttons_dict: dict):
        """
        Adds a keyboard configuration to the storage.

        :param key_in_storage: Unique identifier for the keyboard configuration.
        :type key_in_storage: str

        :param buttons_dict: Dictionary containing the button mappings for the keyboard.
        :type buttons_dict: dict

        :raises ValueError: If the maximum number of allowed keyboard configurations has been reached.
        """
        cls.validate_keyboards_count_in_storage()
        cls.set_buttons_dict(key_in_storage=key_in_storage, buttons_dict=buttons_dict)

    @classmethod
    def set_buttons_dict(cls, key_in_storage: str, buttons_dict: dict):
        """
        Sets a dictionary of buttons for a specific key in the BUTTONS_KEYBOARD_STORAGE.

        :param key_in_storage: The key under which the buttons dictionary will be stored.
        :type key_in_storage: str
        :param buttons_dict: A dictionary containing button configurations.
        :type buttons_dict: dict
        """
        cls.BUTTONS_KEYBOARD_STORAGE[key_in_storage] = buttons_dict

    @classmethod
    def get_buttons_dict(cls, key_in_storage: str) -> dict | None:
        """
        Retrieves a dictionary of buttons associated with a given key.

        :param key_in_storage: The key to retrieve the buttons dictionary for.
        :type key_in_storage: str
        :return: A dictionary containing the buttons or None if the key is not found.
        :rtype: dict | None
        """
        return cls.BUTTONS_KEYBOARD_STORAGE.get(key_in_storage)

    @classmethod
    def validate_keyboards_count_in_storage(cls):
        """
        Validates the count of keyboards in storage.

        This method checks if the number of keyboards in storage is valid and clears the buttons dictionary if it is.
        """
        if cls.check_count_keyboards_in_storage():
            cls.clear_buttons_dict()

    @classmethod
    def check_count_keyboards_in_storage(cls) -> bool:
        """
        Checks if the count of keyboards in storage exceeds a certain threshold.

        :param cls: The class itself.
        :type cls: Any
        :returns: True if the count of keyboards exceeds 5; otherwise, False.
        :rtype: bool
        """
        if len(cls.BUTTONS_KEYBOARD_STORAGE) > 5:
            return True
        return False

    @classmethod
    def clear_buttons_dict(cls):
        """
        Removes the oldest keyboard configuration from storage if the number of stored keyboards exceeds the limit.

        This method checks if the number of stored keyboard configurations exceeds the allowed limit (5).
        If so, it removes the oldest entry (first added key) from the `BUTTONS_KEYBOARD_STORAGE`.

        :raises KeyError: If the storage is empty when attempting to remove a keyboard.
        """
        if len(cls.BUTTONS_KEYBOARD_STORAGE) > 5:
            oldest_key = list(cls.BUTTONS_KEYBOARD_STORAGE.keys())[0]
            cls.BUTTONS_KEYBOARD_STORAGE.pop(oldest_key)

    def create_static_keyboard(self, key: str, lang: str, placeholder: dict = None):
        """
        Creates a static keyboard based on provided configuration.

        :param key: The identifier for the keyboard to be created.
        :type key: str

        :param lang: The language code for the buttons in the keyboard.
        :type lang: str

        :param placeholder: Optional placeholder string for the keyboard.
        :type placeholder: str

        :returns: An InlineKeyboardMarkup or ReplyKeyboardMarkup object, depending on the keyboard type.
        :rtype: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]
        """
        logger.info(f"placeholder: {placeholder}")
        data = Configuration.strings.get("keyboards_list").get(key)
        self._validate_keyboard_type(data.get("keyboard_type"))
        buttons = self.create_buttons(
            data.get("key"), data.get("keyboard_type"), lang=lang, mode="static", placeholder=placeholder
        )
        rows = self._group_buttons_into_fixed_rows(buttons, data.get("row_width") or 1)

        if data.get("keyboard_type") == "inline":
            return InlineKeyboardMarkup(inline_keyboard=rows)
        elif data.get("keyboard_type") == "reply":
            return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

    def create_dynamic_keyboard(
        self, buttons_dict: dict, lang: str, key_in_storage: str, page: int = 1, per_page: int = 5
    ):
        """
        Creates a dynamic keyboard based on custom data from user.

        EXAMPLE:
            buttons_dict = {
                "keyboard_type": "inline",
                "row_width": 2,
                "button": [
                    {
                        "text": "get_admin_menu",
                        "type": "callback",
                        "data": "admin_menu"
                    },
                    {
                        "text": "Перейти",
                        "type": "callback",
                        "data": "projects_menu"
                    }
                ]
            }

        :param buttons_dict: The dict with param: "button" and "keyboard_type"
        :type buttons_dict: dict

        :param lang: The language code for the buttons in the keyboard.
        :type lang: str

        :param key_in_storage: The identifier for the keyboard to be created in `BUTTONS_KEYBOARD_STORAGE`.
        :type key_in_storage: str

        :param page: The current page number for pagination.
        :param per_page: The number of buttons per page.
        :returns: An InlineKeyboardMarkup or ReplyKeyboardMarkup object, depending on the keyboard type.
        :rtype: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]
        """
        # TODO: готов обсудить перемещение передачу keyboard_type из словаря в аргументы метода
        # TODO: готов обсудить также переименование переменной `key` на что-то более подходящее
        # logger.info(f'buttons_dict: {buttons_dict}')
        self.add_keyboard_to_storage(key_in_storage=key_in_storage, buttons_dict=buttons_dict)
        prepare_data = self._get_prepare_data_to_keyboard_data(
            buttons_dict=buttons_dict, lang=lang, page=page, per_page=per_page
        )

        self._validate_keyboard_type(keyboard_type=prepare_data.get("keyboard_type"))

        rows = self._build_keyboard_rows(
            fixed_top_buttons=prepare_data.get("fixed_top_buttons"),
            fixed_bottom_buttons=prepare_data.get("fixed_bottom_buttons"),
            current_buttons=prepare_data.get("current_buttons"),
            total_pages=prepare_data.get("total_pages"),
            page=page,
            key_in_storage=key_in_storage,
        )

        if prepare_data.get("keyboard_type") == "inline":
            return InlineKeyboardMarkup(inline_keyboard=rows)
        elif prepare_data.get("keyboard_type") == "reply":
            return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

    def _get_prepare_data_to_keyboard_data(
        self, buttons_dict: dict, lang: str, page: int, per_page: int, placeholder: dict = None
    ) -> dict:
        """
        Converts prepared data to keyboard data format.

        :param buttons_dict: Dictionary containing the layout and properties of the buttons.
        :type buttons_dict: dict
        :param lang: Language for the button labels.
        :type lang: str
        :param page: Current page number for pagination.
        :type page: int
        :param per_page: Number of items per page for pagination.
        :type per_page: int
        :param placeholder: The placeholder text for the keyboard.
        :type placeholder: dict
        :returns: A dict containing the keyboard type, all buttons, fixed top buttons, fixed bottom buttons, current
        page's buttons, and total pages.
        :rtype: dict
        """
        # logger.info(f'buttons_dict.get(button): {buttons_dict.get("button")}')
        keyboard_type = buttons_dict.get("keyboard_type")
        buttons = self.create_buttons(
            buttons_dict.get("button"), keyboard_type=keyboard_type, lang=lang, mode="dynamic", placeholder=placeholder
        )
        fixed_top_buttons = self.create_buttons(
            buttons_dict.get("fixed_top", []), keyboard_type=keyboard_type, lang=lang, mode="dynamic"
        )
        fixed_bottom_buttons = self.create_buttons(
            buttons_dict.get("fixed_bottom", []), keyboard_type=keyboard_type, lang=lang, mode="dynamic"
        )
        current_buttons, total_pages = self._paginate_buttons(buttons, page, per_page, buttons_dict.get("row_width"))

        return {
            "keyboard_type": keyboard_type,
            "buttons": buttons,
            "fixed_top_buttons": fixed_top_buttons,
            "fixed_bottom_buttons": fixed_bottom_buttons,
            "current_buttons": current_buttons,
            "total_pages": total_pages,
        }

    def create_buttons(
        self, keys: list, keyboard_type: str, lang: str, mode: str, placeholder: dict = None
    ) -> list | None:
        """
        Creates a list of buttons based on the provided keys and keyboard type.

        :param keys: A list of button labels or other identifiers.
        :type keys: list
        :param keyboard_type: The type of keyboard to create buttons for, either "inline" or "reply".
        :type keyboard_type: str
        :param lang: The language in which the buttons should be created.
        :type lang: str
        :param mode: Select a mode: static keyboards or dynamic keyboards.
        :type mode: str
        :param placeholder:
        :type placeholder: dict
        :returns: A list of button objects created using the specified button creator function.
        :rtype: list
        :raises ValueError: If the provided keyboard_type is not one of the allowed values ("inline" or "reply").
        """
        logger.info(f"placeholder: {placeholder}")

        self._validate_keyboard_type(keyboard_type)

        button_creators = self._get_button_creators(mode=mode, placeholder=placeholder)
        logger.info(f"button_creators: {button_creators}")
        buttons = []
        for button in keys:
            logger.info(f"Creating button: {button}")
            button_object = button_creators[keyboard_type](button_data=button, lang=lang, placeholder=placeholder)
            buttons.append(button_object)
        return buttons
        # return [button_creators[keyboard_type](button_data=button, lang=lang) for button in keys]

    def _get_button_creators(self, mode: str, placeholder: dict = None):
        """
        Returns a dictionary of button creation methods based on the mode.

        :param mode: Either "static" or "dynamic"
        :type mode: str
        :returns: Dictionary mapping keyboard types to creation functions.
        :rtype: dict
        """
        if mode == "static":
            return {
                # TODO: проделать тоже самое с reply_button
                "inline": self._create_static_inline_button,
                "reply": self._create_static_reply_button,
            }
        elif mode == "dynamic":
            return {
                "inline": self._create_dynamic_inline_button,
                "reply": self._create_dynamic_reply_button,
            }
        else:
            self._validate_mode(mode)

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
            # TODO: сделать отдельный валидатор
            raise ValueError(f"Кнопка с ключом '{key}' не найдена в YAML.")
        return self.buttons[key]

    def translate_button_text(self, key: str, lang: str) -> str:
        # TODO: написать тест
        """
        Translates button text based on the provided key and language.

        :param key: The key corresponding to the text to be translated.
        :type key: str
        :param lang: The language code (e.g., 'en' for English, 'ru' for Russian) in which the text should be
            translated.
        :type lang: str
        :returns: The translated button text or the original key if no translation is available.
        :rtype: str
        """
        translated_text = self.language_data
        return translated_text.get(lang, {}).get(key, key)

    def _create_static_inline_button(
        self, button_data: str, lang: str, placeholder: dict | None = None
    ) -> InlineKeyboardButton:
        # TODO: написать тест и обновить доку с плейсхолдером
        """
        Creates an inline button for an InlineKeyboard markup.

        :param button_data: A unique identifier for the button.
        :type button_data: str
        :param lang: Language code for text translation.
        :type lang: str
        :returns: An InlineKeyboardButton object with translated text and specified attributes (url or callback_data).
        :rtype: InlineKeyboardButton
        :raises ValueError: If 'text' parameter is missing in button_info.
        :raises ValueError: If neither 'url' nor 'callback_data' is provided in button_info.
        """
        logger.info(f"placeholder: {placeholder}")

        placeholder = placeholder or {}
        button_info = self.get_button_info(button_data)
        self._validate_button_data(button_data=button_info, mode="inline")
        translated_text = self.translate_button_text(button_info.get("text"), lang=lang)
        callback_pattern = button_info.get("data", "")
        callback_data = format_text_with_kwargs(callback_pattern, **placeholder)

        return InlineKeyboardButton(
            text=translated_text,
            url=button_info.get("url"),
            callback_data=callback_data,
        )

    def _create_dynamic_inline_button(
        self, button_data: dict, lang: str, placeholder: dict = None
    ) -> InlineKeyboardButton | None:
        # TODO: написать тест
        # TODO: обработать placeholder
        """
        Creates an inline button for an InlineKeyboard markup.

        :param button_data: Dictionary of button data.
        :type button_data: dict
        :param lang: Language code for text translation.
        :type lang: str
        :returns: An InlineKeyboardButton object with translated text and specified attributes (url or callback_data).
        :rtype: InlineKeyboardButton
        :raises ValueError: If 'text' parameter is missing in button_info.
        :raises ValueError: If neither 'url' nor 'callback_data' is provided in button_info.
        """

        self._validate_button_data(button_data)

        translated_text = self.translate_button_text(button_data["text"], lang=lang)
        button_type = button_data["type"]
        data = button_data.get("data")

        if button_type == "callback":
            self._validate_button_data(button_data=button_data, mode="inline")
            return InlineKeyboardButton(text=translated_text, callback_data=data)

        elif button_type == "url":
            self._validate_button_data(button_data=button_data, mode="inline")
            return InlineKeyboardButton(text=translated_text, url=data)

    def _create_static_reply_button(self, button_data: str, lang: str, placeholder: dict = None) -> KeyboardButton:
        # TODO: написать тест
        """
        Creates a reply button with translated text.

        :param button_data: The identifier for the button.
        :type button_data: str
        :param lang: The language code to translate the button text into.
        :type lang: str
        :returns: A KeyboardButton instance with the translated text.
        :rtype: KeyboardButton
        """
        # TODO: пришлось переименовать с `key` на `button_data`, потому что такой аргумент обрабатывается в динамической
        #  клавиатуре и для единства пока так
        button_info = self.get_button_info(button_data)
        translated_text = self.translate_button_text(button_info.get("text"), lang=lang)
        return KeyboardButton(text=translated_text)

    def _create_dynamic_reply_button(self, button_data: dict, lang: str, placeholder: dict = None) -> KeyboardButton:
        # TODO: написать тест
        """
        Creates a reply button with translated text.

        :param button_data: Dictionary of button data.
        :type button_data: dict
        :param lang: The language code to translate the button text into.
        :type lang: str
        :returns: A KeyboardButton instance with the translated text.
        :rtype: KeyboardButton
        """
        self._validate_button_data(button_data=button_data, mode="reply")

        translated_text = self.translate_button_text(button_data.get("text"), lang=lang)
        return KeyboardButton(text=translated_text)

    def _paginate_buttons(self, buttons: list, page: int, per_page: int, row_width):
        """
        Paginates the given list of buttons.

        :param buttons: List of all buttons
        :param page: Current page number.
        :param per_page: Number of buttons per page.
        :param row_width: Row width settings
        :return: Tuple (paginated buttons as rows, total pages)
        """
        total_pages = ceil(len(buttons) / per_page) if buttons else 1
        page = max(1, min(page, total_pages))

        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        current_buttons = buttons[start_idx:end_idx]

        rows = self._group_buttons_for_layout(current_buttons, row_width)

        return rows, total_pages

    def _build_keyboard_rows(
        self,
        fixed_top_buttons: list,
        fixed_bottom_buttons: list,
        current_buttons: list,
        total_pages: int,
        page: int,
        key_in_storage: str,
    ):
        """
        Forms rows of buttons for an order and data display.

        :param fixed_top_buttons: List of fixed buttons to be displayed at the top.
        :type fixed_top_buttons: list

        :param fixed_bottom_buttons: List of fixed buttons to be displayed at the bottom.
        :type fixed_bottom_buttons: list

        :param current_buttons: List of buttons to be displayed, divided by pages.
        :type current_buttons: list

        :param total_pages: Total number of pages for pagination.
        :type total_pages: int

        :param page: Current page number.
        :type page: int

        :param key_in_storage: Key to find buttons_dict in `BUTTONS_KEYBOARD_STORAGE`.
        :type key_in_storage: str

        :returns: Rows of buttons with fixed and current buttons.
        :rtype: list

        :raises TypeError: If any parameter is not of the expected type.
        """
        rows = []

        if fixed_top_buttons:
            rows.append(fixed_top_buttons)

        rows.extend(current_buttons)

        # Добавляем кнопки пагинации
        pagination_buttons = self._get_pagination_buttons(
            page=page, total_pages=total_pages, key_in_storage=key_in_storage
        )
        if pagination_buttons:
            rows.append(pagination_buttons)

        # Добавляем фиксированные кнопки снизу
        if fixed_bottom_buttons:
            rows.append(fixed_bottom_buttons)

        return rows

    @staticmethod
    def _get_pagination_buttons(page: int, total_pages: int, key_in_storage: str):
        """
        Generates pagination buttons.

        :param page: Current page number
        :param total_pages: Total number of pages
        :param key_in_storage: Key to find in `BUTTONS_KEYBOARD_STORAGE`.
        :return: List of pagination buttons
        """
        # if total_pages <= 1:
        #     return []
        empty_button = InlineKeyboardButton(text=" ", callback_data="noop")
        pagination_buttons = [
            (
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=Pagination.create(page=page - 1, key_in_storage=key_in_storage),
                )
                if page > 1
                else empty_button
            ),
            InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="noop"),
            (
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=Pagination.create(page=page + 1, key_in_storage=key_in_storage),
                )
                if page < total_pages
                else empty_button
            ),
        ]
        return pagination_buttons

    def _group_buttons_for_layout(self, buttons: list, row_width):
        """
        Groups buttons into rows based on row width settings.

        :param buttons: List of buttons to be grouped.
        :param row_width: Row width settings.
        :return: List of grouped buttons.
        """
        if isinstance(row_width, list):
            return self._group_buttons_by_custom_rows(buttons, row_width)
        return self._group_buttons_into_fixed_rows(buttons, row_width or 1)

    @staticmethod
    def _group_buttons_into_fixed_rows(buttons: list, row_width: int) -> list:
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

    @staticmethod
    def _group_buttons_by_custom_rows(buttons: list, row_structure: list) -> list:
        """
        Groups buttons according to a custom row structure.

        :param buttons: List of buttons
        :param row_structure: List specifying how many buttons should be in each row
        :return: List of grouped buttons
        """
        rows = []
        index = 0

        for count in row_structure:
            row = buttons[index : index + count]
            rows.append(row)
            index += count

            if index >= len(buttons):
                break

        return rows

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

    @staticmethod
    def _validate_button_data(button_data: dict, mode: str = None):
        """
        Validates the data for a button based on its mode.

        :param button_data: A dictionary containing the button data to be validated.
        :type button_data: dict
        :param mode: The mode in which the button is used, can be "reply" or "inline". Optional.
        :type mode: str
        """
        KeyboardGenerator._validate_common_button_fields(button_data)

        if mode == "reply":
            KeyboardGenerator._validate_reply_button(button_data)
        elif mode == "inline":
            KeyboardGenerator._validate_inline_button(button_data)

    @staticmethod
    def _validate_common_button_fields(button_data: dict):
        """
        Validates the common fields for a button.

        :param button_data: A dictionary containing data about the button.
        :type button_data: dict
        :raises ValueError: If the 'text' parameter is missing in the button data.
        :raises ValueError: If the 'type' parameter is missing in the button data.
        """
        # logger.info(f"button data: {button_data}.")
        if not button_data.get("text"):
            raise ValueError("Отсутствует обязательный параметр 'text' в кнопке")

        if "type" not in button_data:
            raise ValueError("Отсутствует параметр 'type' в кнопке (callback, url, text и др.)")

    @staticmethod
    def _validate_reply_button(button_data: dict):
        """
        Validates the data for a reply button.

        :param button_data: Data dictionary containing the button information.
        :type button_data: dict
        :returns: None if all checks pass.
        :rtype: None
        :raises ValueError: If the 'text' parameter is missing in the button data or if the 'type' parameter is missing.
        """
        if not button_data.get("text"):
            raise ValueError("Отсутствует обязательный параметр 'text' в reply-кнопке")
        if "type" not in button_data:
            raise ValueError("Отсутствует параметр 'type' в reply-кнопке (callback, url, text и др.)")

    @staticmethod
    def _validate_inline_button(button_data: dict):
        """
        Validates the data for an inline button.

        :param button_data: Dictionary containing the button data.
        :type button_data: dict
        :raises ValueError: If 'data' is missing for a 'callback' type button.
        :raises ValueError: If the length of 'data' exceeds 64 characters for a 'callback' type button.
        :raises ValueError: If 'data' is missing or not a string for an 'url' type button.
        """
        button_type = button_data.get("type")
        data = button_data.get("data")

        if button_type == "callback":
            if not data:
                raise ValueError("Для callback-кнопки необходимо указать 'data'")
            if len(data) > 64:
                raise ValueError(f"Длина callback_data превышает 64 символа: {data}")
        elif button_type == "url":
            if not data or not isinstance(data, str):
                raise ValueError("Для URL-кнопки необходимо указать корректный 'data' (URL)")

    @staticmethod
    def _validate_mode(mode):
        if mode not in ["static", "dynamic"]:
            raise ValueError(f"Недопустимый режим: {mode}")


"""
EXAMPLE CONFIG KEYBOARDS:
1. Dynamic generation keyboards - Simple:

buttons_dict = {
    "keyboard_type": "inline",
    "row_width": 1,
    "button": [
        {
            "text": "1",
            "type": "callback",
            "data": "admin_menu"
        },
    ]
}

2. Dynamic generation keyboards with pagination:

buttons_dict = {
    "keyboard_type": "inline",  # select a type of a keyboards
    "row_width": [1, 1, 1, 1, 1],

    # Creates a layout scheme for entity elements (such as an event or an admin).
    # The number of digits indicates the number of entity rows (excluding pagination and fixed rows), while the digit
    # values specify the allowed number of elements per row.

    "fixed_top": [
        {"text": " ", "type": "callback", "data": "noop"},
        {"text": "Admin menu", "type": "callback", "data": "noop"},
        {"text": " ", "type": "callback", "data": "noop"},
    ],
    #     Sets a fixed (pinned) button for the keyboard.

    "button": [
        {"text": f"Button {i + 1}", "type": "callback", "data": f"action_{i + 1}"}
        for i in range(10)
    ],
    #     The main array of buttons.

    "fixed_bottom": [
        {"text": "Back to menu", "type": "callback", "data": "menu"},
        {"text": "Add admin", "type": "callback", "data": "add_admin"},

    ]
    #     Sets a fixed (pinned) button for the keyboard.
}

Example for create_keyboards:
1. Static keyboards:
await message.answer(
    Configuration.strings.get("messages_text").get("message_to_start"),
    reply_markup=keyboard.create_static_keyboard(key="started_keyboard", lang="en"),
)

2. Dynamic keyboards:
await message.answer(
    Configuration.strings.get("messages_text").get("message_to_start"),
    reply_markup=keyboard.create_dynamic_keyboard(buttons_dict=buttons_dict, lang="en"),
)
"""
