from aiogram import Router

from src.logic.bot_logic.handlers.profile_handlers.profile_handlers import profile_router

main_profile_router = Router()
main_profile_router.include_routers(profile_router)
