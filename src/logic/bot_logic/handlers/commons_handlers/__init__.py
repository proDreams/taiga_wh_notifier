from aiogram import Router

from src.logic.bot_logic.handlers.commons_handlers.commands_handlers import router

common_router = Router()
common_router.include_routers(router)
