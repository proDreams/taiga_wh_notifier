from aiogram.filters.callback_data import CallbackData

from src.entities.enums.handlers_enum import PaginationButtonsEnum


class MenuData(CallbackData, prefix="menu"):
    pass


class NoMoveData(CallbackData, prefix="no_move"):
    action: PaginationButtonsEnum
    page: int | None = None
    all_pages: int | None = None
