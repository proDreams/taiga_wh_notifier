from aiogram import Router

from src.logic.bot_logic.handlers.admins_handlers.admins_handlers import admin_router

main_admin_router = Router()
main_admin_router.include_routers(admin_router)
