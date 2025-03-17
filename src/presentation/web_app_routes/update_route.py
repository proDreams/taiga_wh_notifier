from aiogram.types import Update
from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from src.core.settings import Configuration

update_router = APIRouter()


@update_router.post(Configuration.settings.UPDATES_PATH, status_code=status.HTTP_200_OK)
async def webhook(update: Update) -> Response:
    """
    Handles webhook requests from Telegram.

    :param update: The incoming Update object containing information about the event.
    :type update: Update
    :return: A response indicating successful processing of the update.
    :rtype: Response
    """
    await Configuration.dispatcher.feed_update(Configuration.bot, update)

    return Response(status_code=status.HTTP_200_OK)
