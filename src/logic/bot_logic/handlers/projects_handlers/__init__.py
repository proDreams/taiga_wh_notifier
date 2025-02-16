from aiogram import Router

from src.logic.bot_logic.handlers.projects_handlers.projects_handlers import projects_router

main_projects_router = Router()
main_projects_router.include_routers(projects_router)
