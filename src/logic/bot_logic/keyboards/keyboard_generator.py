import importlib
from math import ceil
from typing import Any

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.core.Base.singleton import Singleton
from src.core.settings import Configuration
from src.entities.callback_classes.menu_callbacks import MenuData, NoMoveData
from src.entities.enums.handlers_enum import PaginationButtonsEnum
from src.entities.enums.keyboard_enum import KeyboardTypeEnum
from src.utils.text_utils import localize_text_to_button


class KeyboardGenerator(Singleton):
    def __init__(self):
        self._static_keyboards = Configuration.strings.get("static_keyboards")
        self._dynamic_keyboards = Configuration.strings.get("dynamic_keyboards")
        self.page_limit = Configuration.settings.ITEMS_PER_PAGE

    @staticmethod
    async def _get_menu_button(lang: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=localize_text_to_button(text_in_yaml="get_main_menu", lang=lang),
            callback_data=MenuData().pack(),
        )

    @staticmethod
    def _get_callback_class(callback_cls: str) -> type[CallbackData]:
        module = importlib.import_module("src.entities.callback_classes")
        return getattr(module, callback_cls)

    async def _get_pagination_buttons(
        self, page: int, pagination_class: str, lang: str, count: int, **kwargs
    ) -> list[InlineKeyboardButton]:
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
        return InlineKeyboardButton(text=" ", callback_data=NoMoveData(action=PaginationButtonsEnum.BLANK).pack())

    async def _generate_keyboard_header(self, builder: InlineKeyboardBuilder, text: str, lang: str):
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
    async def _get_static_reply_button(text_key: str, lang: str) -> KeyboardButton:
        return KeyboardButton(text=localize_text_to_button(text_in_yaml=text_key, lang=lang))

    async def _get_static_inline_button(
        self, button: dict[str, str], text_key: str, lang: str, **kwargs
    ) -> InlineKeyboardButton:
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
        args_dict = {arg: getattr(data_row, arg) for arg in data_args}
        text = getattr(data_row, data_text_field)

        return InlineKeyboardButton(text=text, callback_data=callback_cls(**args_dict).pack())

    async def _generate_static_buttons_row(
        self, builder: InlineKeyboardBuilder, buttons_list: list, kb_type: KeyboardTypeEnum, lang: str, **kwargs
    ) -> InlineKeyboardBuilder:
        for row in buttons_list:
            buttons_lst = []

            for button in row:
                text_key = button.get("text")

                match kb_type:
                    case KeyboardTypeEnum.REPLY:
                        buttons_lst.append(await self._get_static_reply_button(text_key=text_key, lang=lang))
                    case KeyboardTypeEnum.INLINE:
                        buttons_lst.append(
                            await self._get_static_inline_button(button=button, text_key=text_key, lang=lang, **kwargs)
                        )

            builder.row(*buttons_lst)

        return builder

    async def generate_static_keyboard(self, kb_key: str, lang: str, **kwargs) -> InlineKeyboardMarkup:
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

        if pagination_class := kb_data.get("pagination_class"):
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
