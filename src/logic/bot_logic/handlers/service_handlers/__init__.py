from aiogram import Router

from src.logic.bot_logic.handlers.service_handlers.service_errors_handler import service_errors_router
from src.logic.bot_logic.handlers.service_handlers.service_events_handlers import service_events_router

main_service_router = Router()

main_service_router.include_routers(service_events_router, service_errors_router)
