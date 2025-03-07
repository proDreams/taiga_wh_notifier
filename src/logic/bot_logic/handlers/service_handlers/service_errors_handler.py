from aiogram import Router
from aiogram.types import ErrorEvent

from src.core.settings import get_logger, get_settings
from src.utils.send_message_utils import send_message
from src.utils.text_utils import get_service_text

service_errors_router = Router()

logger = get_logger(name=__name__)


@service_errors_router.error()
async def error_handler(event: ErrorEvent) -> None:
    logger.critical("Ошибка: %s", event.exception, exc_info=True)
    await send_message(
        chat_id=get_settings().ERRORS_CHAT_ID,
        message_thread_id=get_settings().ERRORS_THREAD_ID,
        text=get_service_text(text_in_yaml="error_message", exception=event.exception),
    )
