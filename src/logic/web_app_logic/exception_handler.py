from fastapi import FastAPI, Request

from src.core.Base.exceptions import MessageFormatterError
from src.core.settings import get_logger, get_settings
from src.utils.send_message_utils import send_message
from src.utils.text_utils import get_service_text

logger = get_logger(name=__name__)


async def handling_exceptions(app: FastAPI) -> FastAPI:
    @app.exception_handler(MessageFormatterError)
    async def handle_exception(request: Request, exc: MessageFormatterError):
        logger.critical("Error: %s", exc.message, exc_info=True)
        await send_message(
            chat_id=get_settings().ERRORS_CHAT_ID,
            message_thread_id=get_settings().ERRORS_THREAD_ID,
            text=get_service_text(text_in_yaml="error_message", exception=exc.message),
        )

    return app
