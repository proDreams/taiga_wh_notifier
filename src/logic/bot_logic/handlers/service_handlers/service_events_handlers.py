from aiogram import Router

from src.core.settings import get_settings
from src.utils.send_message_utils import send_message
from src.utils.text_utils import get_service_text

service_events_router = Router()


@service_events_router.startup()
async def start_bot() -> None:
    for admin_id in get_settings().ADMIN_IDS:
        await send_message(chat_id=admin_id, text=get_service_text(text_in_yaml="start_bot_notification"))


@service_events_router.shutdown()
async def stop_bot() -> None:
    for admin_id in get_settings().ADMIN_IDS:
        await send_message(chat_id=admin_id, text=get_service_text(text_in_yaml="stop_bot_notification"))
