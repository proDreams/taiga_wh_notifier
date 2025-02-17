from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from src.entities.schemas.user_data.user_schemas import UserCreateSchema
from src.logic.services.user_service import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        user_obj = UserCreateSchema(**user.model_dump(), telegram_id=user.id)
        data["user"] = await UserService().get_or_create_user(user=user_obj)
        return await handler(event, data)
