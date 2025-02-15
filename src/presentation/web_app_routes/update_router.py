from aiogram.types import Update
from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from src.core.settings import Configuration

update_router = APIRouter()


@update_router.post("/update", status_code=status.HTTP_200_OK)
async def webhook(update: Update) -> Response:
    await Configuration.dispatcher.feed_update(Configuration.bot, update)

    return Response(status_code=status.HTTP_200_OK)
