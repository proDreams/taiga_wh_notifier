from aiogram.filters.callback_data import CallbackData

from src.entities.enums.handlers_enum import PaginationButtonsEnum


class MenuData(CallbackData, prefix="menu"):
    """
    Represents menu data for a callback interface.
    """

    pass


class NoMoveData(CallbackData, prefix="no_move"):
    """
    Represents callback data without any action.

    :param action: The specific pagination action to be performed.
    :type action: PaginationButtonsEnum
    :param page: The current page number if applicable.
    :type page: int | None
    :param all_pages: Total number of pages available if applicable.
    :type all_pages: int | None
    """

    action: PaginationButtonsEnum
    page: int | None = None
    all_pages: int | None = None
