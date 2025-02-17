from aiogram.filters.callback_data import CallbackData


class Pagination(CallbackData, prefix="page"):
    page: int
    key_in_storage: str

    @classmethod
    def create(cls, page: int, key_in_storage: str) -> str:
        """
        Creates a callback_data for pagination button.

        :param page: The page number.
        :type page: int
        :param key_in_storage: A unique identifier for the instance of keyboard.
        :type key_in_storage: str
        :return: Packed representation of the created object.
        :rtype: str
        """
        return cls(page=page, key_in_storage=key_in_storage).pack()
