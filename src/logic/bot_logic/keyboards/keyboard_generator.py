import importlib
import json
from math import ceil
from typing import Any

from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestUsers,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.core.Base.singleton import Singleton
from src.core.settings import get_settings, get_strings
from src.entities.callback_classes.checkbox_callbacks import CheckboxData
from src.entities.callback_classes.menu_callbacks import MenuData, NoMoveData
from src.entities.enums.handlers_enum import PaginationButtonsEnum
from src.entities.enums.keyboard_enum import KeyboardTypeEnum
from src.utils.text_utils import localize_text_to_button


class KeyboardGenerator(Singleton):
    """
    Class for generating keyboard layouts based on configuration data.
    """

    def __init__(self):
        """Class for managing different types of keyboards."""
        self._static_keyboards = get_strings().get("static_keyboards")
        self._dynamic_keyboards = get_strings().get("dynamic_keyboards")
        self._checkbox_keyboards = get_strings().get("checkbox_keyboards")
        self.page_limit = get_settings().ITEMS_PER_PAGE

    @staticmethod
    async def _get_menu_button(lang: str) -> InlineKeyboardButton:
        """
        Creates an inline keyboard button for accessing the main menu.

        :param lang: Language code to determine which text should be used for the button.
        :type lang: str
        :return: An InlineKeyboardButton object configured with localized text and a callback data payload.
        :rtype: InlineKeyboardButton
        """
        return InlineKeyboardButton(
            text=localize_text_to_button(text_in_yaml="get_main_menu", lang=lang),
            callback_data=MenuData().pack(),
        )

    @staticmethod
    def _get_callback_class(callback_cls: str) -> type[CallbackData]:
        """
        Retrieves a callback class based on its name.

        :param callback_cls: Name of the callback class to be retrieved.
        :type callback_cls: str
        :returns: The callback class corresponding to the given name.
        :rtype: type[CallbackData]
        :raises ImportError: If the module 'src.entities.callback_classes' cannot be imported.
        """
        module = importlib.import_module("src.entities.callback_classes")
        return getattr(module, callback_cls)

    async def _get_pagination_buttons(
        self, page: int, pagination_class: str, lang: str, count: int, **kwargs
    ) -> list[InlineKeyboardButton]:
        """
        Generates pagination buttons for an inline keyboard.

        :param page: The current page number.
        :type page: int
        :param pagination_class: The class name used to create callback data.
        :type pagination_class: str
        :param lang: The language code for localization purposes.
        :type lang: str
        :param count: The total number of items to be paginated.
        :type count: int
        :return: A list of InlineKeyboardButton objects representing pagination controls.
        :rtype: list[InlineKeyboardButton]
        """
        callback_cls = self._get_callback_class(callback_cls=pagination_class)

        pagination_buttons = []

        if page > 0:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=localize_text_to_button(text_in_yaml="previous", lang=lang),
                    callback_data=callback_cls(page=page - 1, **kwargs).pack(),
                )
            )
        else:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=localize_text_to_button(text_in_yaml="no_move", lang=lang),
                    callback_data=NoMoveData(action=PaginationButtonsEnum.NO_BACK).pack(),
                )
            )

        page_count = ceil(count / self.page_limit)

        pagination_buttons.append(
            InlineKeyboardButton(
                text=f"{page + 1}/{page_count}",
                callback_data=NoMoveData(
                    action=PaginationButtonsEnum.JUST_INFO, page=page + 1, all_pages=page_count
                ).pack(),
            )
        )

        if page + 1 < page_count:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=localize_text_to_button(text_in_yaml="next", lang=lang),
                    callback_data=callback_cls(page=page + 1, **kwargs).pack(),
                )
            )
        else:
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=localize_text_to_button(text_in_yaml="no_move", lang=lang),
                    callback_data=NoMoveData(action=PaginationButtonsEnum.NO_NEXT).pack(),
                )
            )

        return pagination_buttons

    @staticmethod
    async def _get_blank_button() -> InlineKeyboardButton:
        """
        Returns an InlineKeyboardButton representing a blank button.
        """
        return InlineKeyboardButton(text=" ", callback_data=NoMoveData(action=PaginationButtonsEnum.BLANK).pack())

    async def _generate_keyboard_header(self, builder: InlineKeyboardBuilder, text: str, lang: str):
        """
        Generates a keyboard header with blank buttons and localized text.

        :param builder: InlineKeyboardBuilder object to build the keyboard.
        :type builder: InlineKeyboardBuilder
        :param text: Text to be displayed on the button, specified in YAML.
        :type text: str
        :param lang: Language code for localization of the button text.
        :type lang: str
        :return: The configured InlineKeyboardBuilder instance with the header row added.
        :rtype: InlineKeyboardBuilder
        """
        builder.row(
            await self._get_blank_button(),
            InlineKeyboardButton(
                text=localize_text_to_button(text_in_yaml=text, lang=lang),
                callback_data=NoMoveData(action=PaginationButtonsEnum.BLANK).pack(),
            ),
            await self._get_blank_button(),
        )

        return builder

    @staticmethod
    async def _get_static_reply_button(
        text_key: str, lang: str, request_users: bool | None = None, **kwargs
    ) -> KeyboardButton:
        """
        Creates a static reply button for user interaction.

        :param text_key: Key to the localized text used as the button label.
        :type text_key: str
        :param lang: Language code to fetch the localized text.
        :type lang: str
        :param request_users: Optional boolean flag indicating if the button should request users.
        :type request_users: bool | None
        :param kwargs: Additional keyword arguments that might be needed for creating a request.
        :type kwargs: Any
        :returns: A KeyboardButton instance configured with the specified parameters.
        :rtype: KeyboardButton
        """
        if request_users:
            request_users = KeyboardButtonRequestUsers(
                request_id=kwargs.get("request_id"), max_quantity=10, request_name=True
            )

        return KeyboardButton(
            text=localize_text_to_button(text_in_yaml=text_key, lang=lang), request_users=request_users
        )

    async def _get_static_inline_button(
        self, button: dict[str, str], text_key: str, lang: str, **kwargs
    ) -> InlineKeyboardButton:
        """
        Create a static inline button for an InlineKeyboard.

        :param button: Dictionary containing the button's configuration.
            Required keys are 'callback_class' and optionally 'args'.
        :type button: dict[str, str]
        :param text_key: The key used to retrieve the button text from localization files.
        :type text_key: str
        :param lang: Language code for which the button text should be localized.
        :type lang: str
        :param kwargs: Additional keyword arguments that may be required by the callback class.
        :type kwargs: dict
        :returns: An InlineKeyboardButton configured according to the provided parameters.
        :rtype: InlineKeyboardButton
        """
        callback_cls = self._get_callback_class(callback_cls=button.get("callback_class"))
        args = button.get("args")

        if args:
            args = {key: kwargs[key] for key in args if key in kwargs}
        else:
            args = {}

        return InlineKeyboardButton(
            text=localize_text_to_button(text_in_yaml=text_key, lang=lang),
            callback_data=callback_cls(**args).pack(),
        )

    @staticmethod
    async def _get_dynamic_inline_button(
        data_row: Any, data_args: list[str], callback_cls: type[CallbackData], data_text_field: str
    ) -> InlineKeyboardButton:
        """
        Creates an InlineKeyboardButton dynamically based on provided data row and arguments.

        :param data_row: An object containing the data fields for the button.
        :type data_row: Any
        :param data_args: A list of strings representing attribute names to extract from data_row.
        :type data_args: list[str]
        :param callback_cls: The callback class type to use for creating the callback_data.
        :type callback_cls: type[CallbackData]
        :param data_text_field: The name of the attribute in data_row that contains the button text.
        :type data_text_field: str
        :returns: An InlineKeyboardButton configured with extracted text and packed callback data.
        :rtype: InlineKeyboardButton
        """
        args_dict = {arg: getattr(data_row, arg) for arg in data_args}
        text = getattr(data_row, data_text_field)

        return InlineKeyboardButton(text=text, callback_data=callback_cls(**args_dict).pack())

    async def _generate_static_buttons_row(
        self,
        builder: InlineKeyboardBuilder | ReplyKeyboardBuilder,
        buttons_list: list,
        kb_type: KeyboardTypeEnum,
        lang: str,
        **kwargs,
    ) -> InlineKeyboardBuilder | ReplyKeyboardBuilder:
        """
        Generates a static row of buttons for inline or reply keyboards.

        :param builder: The keyboard builder object (InlineKeyboardBuilder or ReplyKeyboardBuilder).
        :type builder: InlineKeyboardBuilder | ReplyKeyboardBuilder
        :param buttons_list: List of button configurations, where each element is a list of button dictionaries.
        :type buttons_list: list
        :param kb_type: Type of the keyboard (either KeyboardTypeEnum.REPLY or KeyboardTypeEnum.INLINE).
        :type kb_type: KeyboardTypeEnum
        :param lang: Language code for localization purposes.
        :type lang: str
        :returns: The updated keyboard builder with added buttons.
        :rtype: InlineKeyboardBuilder | ReplyKeyboardBuilder
        """
        for row in buttons_list:
            buttons_lst = []

            for button in row:
                text_key = button.get("text")

                match kb_type:
                    case KeyboardTypeEnum.REPLY:
                        buttons_lst.append(
                            await self._get_static_reply_button(
                                text_key=text_key, lang=lang, request_users=button.get("request_users"), **kwargs
                            )
                        )
                    case KeyboardTypeEnum.INLINE:
                        buttons_lst.append(
                            await self._get_static_inline_button(button=button, text_key=text_key, lang=lang, **kwargs)
                        )

            builder.row(*buttons_lst)

        return builder

    async def generate_static_keyboard(self, kb_key: str, lang: str, **kwargs) -> InlineKeyboardMarkup:
        """
        Generates a static keyboard markup for Telegram bots.

        :param kb_key: The unique key identifying the keyboard configuration.
        :type kb_key: str
        :param lang: The language code to use for button labels and menu buttons.
        :type lang: str
        :param kwargs: Additional keyword arguments that can be used to customize the keyboard generation.
        :return: A `InlineKeyboardMarkup` object representing the generated static keyboard.
        :rtype: InlineKeyboardMarkup
        :raises ValueError: If an unknown keyboard type is encountered in the configuration data.
        """
        kb_data = self._static_keyboards.get(kb_key)
        kb_type = kb_data.get("keyboard_type")

        match kb_type:
            case KeyboardTypeEnum.REPLY:
                builder = ReplyKeyboardBuilder()
            case KeyboardTypeEnum.INLINE:
                builder = InlineKeyboardBuilder()
            case _:
                raise ValueError(f"Unknown keyboard type: {kb_type}")

        builder = await self._generate_static_buttons_row(
            builder=builder,
            buttons_list=kb_data.get("buttons_list"),
            kb_type=kb_type,
            lang=lang,
            **kwargs,
        )

        if kb_data.get("menu_button"):
            builder.row(await self._get_menu_button(lang=lang))

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    async def _generate_dynamic_buttons(
        self, builder: InlineKeyboardBuilder, data: list, data_callback: str, data_args: list[str], data_text_field: str
    ) -> InlineKeyboardBuilder:
        """
        Generates dynamic inline keyboard buttons based on provided data.

        :param builder: An instance of InlineKeyboardBuilder to build the keyboard.
        :type builder: InlineKeyboardBuilder
        :param data: List of data rows to generate buttons from.
        :type data: list
        :param data_callback: The callback class or function name for button clicks.
        :type data_callback: str
        :param data_args: List of additional arguments to pass to the callback.
        :type data_args: list[str]
        :param data_text_field: Field in each data row from which to extract text for button labels.
        :type data_text_field: str
        :returns: The configured InlineKeyboardBuilder with dynamically generated buttons.
        :rtype: InlineKeyboardBuilder
        """
        callback_cls = self._get_callback_class(data_callback)

        for row in data:
            builder.row(
                await self._get_dynamic_inline_button(
                    data_row=row, data_args=data_args, callback_cls=callback_cls, data_text_field=data_text_field
                )
            )

        return builder

    async def generate_dynamic_keyboard(
        self, kb_key: str, data: list, lang: str, page: int | None = None, count: int | None = None, **kwargs
    ) -> InlineKeyboardMarkup:
        """
        Generates a dynamic inline keyboard based on the provided data and configuration.

        :param kb_key: The key identifying the specific keyboard configuration.
        :type kb_key: str
        :param data: The list of data entries to be used in the keyboard buttons.
        :type data: list
        :param lang: The language code for localization purposes.
        :type lang: str
        :param page: The current page number, used for pagination (default is None).
        :type page: int | None
        :param count: The total count of items, used for pagination (default is None).
        :type count: int | None
        **kwargs: Additional keyword arguments for further customization.
        :returns: An InlineKeyboardMarkup object representing the generated keyboard.
        :rtype: InlineKeyboardMarkup
        """
        kb_data = self._dynamic_keyboards.get(kb_key)

        builder = InlineKeyboardBuilder()

        if header_text := kb_data.get("header_text"):
            builder = await self._generate_keyboard_header(builder=builder, text=header_text, lang=lang)

        builder = await self._generate_dynamic_buttons(
            builder=builder,
            data=data,
            data_callback=kb_data.get("data_callback"),
            data_args=kb_data.get("data_args"),
            data_text_field=kb_data.get("data_text_field"),
        )

        if (pagination_class := kb_data.get("pagination_class")) and count > self.page_limit:
            builder.row(
                *await self._get_pagination_buttons(
                    page=page, pagination_class=pagination_class, count=count, lang=lang, **kwargs
                )
            )

        builder = await self._generate_static_buttons_row(
            builder=builder,
            buttons_list=kb_data.get("buttons_list"),
            kb_type=KeyboardTypeEnum.INLINE,
            lang=lang,
            **kwargs,
        )

        if kb_data.get("menu_button"):
            builder.row(await self._get_menu_button(lang=lang))

        return builder.as_markup(resize_keyboard=False, one_time_keyboard=True)

    async def generate_checkbox_keyboard(
        self,
        kb_key: str,
        selected_ids: list[int],
        lang: str,
        ok_button_text: str = "ok",
        **kwargs,
    ) -> InlineKeyboardMarkup:
        """
        Generates an interactive checkbox keyboard with confirmation button.

        :param kb_key: The unique key identifying the keyboard configuration.
        :type kb_key: str
        :param selected_ids: Currently selected item IDs
        :type selected_ids: list[str]
        :param lang: Language for localization
        :type lang: str
        :param ok_button_text: Localization key for OK button
        :type ok_button_text: str
        :return: Configured inline keyboard markup
        :rtype: InlineKeyboardMarkup
        """
        builder = InlineKeyboardBuilder()
        kb_data = self._checkbox_keyboards.get(kb_key)
        buttons_list = kb_data.get("buttons_list")
        # Add checkbox buttons
        items = list(zip(kb_data.get("items"), kb_data.get("ids")))
        for text, item_id in items:
            display_text = localize_text_to_button(
                text_in_yaml=text,
                lang=lang,
            )
            is_selected = item_id in selected_ids
            new_selection = self._toggle_selection(selected_ids, item_id)
            builder.row(
                InlineKeyboardButton(
                    text=f"{'✅' if is_selected else '⬜'} {display_text}",
                    callback_data=CheckboxData(selected_ids=json.dumps(new_selection), action="toggle").pack(),
                )
            )

        # Add OK button
        builder.row(
            InlineKeyboardButton(
                text=localize_text_to_button(ok_button_text, lang),
                callback_data=CheckboxData(selected_ids=json.dumps(selected_ids), action="confirm").pack(),
            )
        )
        for row in buttons_list:
            buttons = []
            for button in row:
                text_key = button.get("text")
                buttons.append(
                    await self._get_static_inline_button(button=button, text_key=text_key, lang=lang, **kwargs),
                )
        builder.row(*buttons)
        return builder.as_markup()

    def _toggle_selection(self, current: list[str], item_id: str) -> list[str]:
        """Helper method to toggle item selection"""
        return [i for i in current if i != item_id] if item_id in current else [*current, item_id]
