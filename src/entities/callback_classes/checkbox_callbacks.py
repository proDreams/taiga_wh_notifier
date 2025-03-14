from aiogram.filters.callback_data import CallbackData


class CheckboxData(CallbackData, prefix="checkbox"):
    """
    Handles checkbox selection data.

    :param selected_ids: List of selected checkbox IDs
    :type selected_ids: str  # Stored as JSON string for callback compatibility
    :param action: Type of checkbox action (toggle/confirm)
    :type action: str
    """

    selected_ids: str
    action: str
