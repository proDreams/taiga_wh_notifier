from aiogram import Router

from src.logic.bot_logic.handlers.commons_handlers import common_router

handlers_router = Router()
handlers_router.include_router(common_router)
