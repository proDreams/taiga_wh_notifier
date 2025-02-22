from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from src.core.settings import Configuration
from src.entities.schemas.user_data.user_schemas import UserCreateSchema
from src.logic.services.user_service import UserService


class UserMiddleware(BaseMiddleware):
    """
    Handles user-related logic in the application.

    This middleware processes user data and ensures that user information is correctly managed before handling any request.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """
        Asynchronously handles Telegram events by wrapping the provided handler function.

        :param handler: A callable that processes a Telegram event and data dictionary.
        :type handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]
        :param event: The Telegram object representing the event to be handled.
        :type event: TelegramObject
        :param data: A dictionary containing additional data related to the event.
        :type data: dict[str, Any]
        :returns: The result of the handler function.
        :rtype: Any
        """
        user: User = data.get("event_from_user")
        user_obj = UserCreateSchema(
            **user.model_dump(), telegram_id=user.id, is_admin=user.id in Configuration.settings.ADMIN_IDS
        )
        data["user"] = await UserService().get_or_create_user(user=user_obj)
        return await handler(event, data)
