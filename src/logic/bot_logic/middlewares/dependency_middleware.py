from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.logic.bot_logic.keyboards.keyboard_generator import KeyboardGenerator
from src.logic.services.user_service import UserService


class DependencyMiddleware(BaseMiddleware):
    """
    Middleware for dependency injection in Telegram bot handlers.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["user"] = await UserService().get_or_create_user(user=data.get("event_from_user"))
        data["keyboard_generator"] = KeyboardGenerator()
        return await handler(event, data)
