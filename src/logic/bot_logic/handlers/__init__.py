from aiogram import Router

from src.logic.bot_logic.handlers.admins_handlers import main_admin_router
from src.logic.bot_logic.handlers.commons_handlers import common_router
from src.logic.bot_logic.handlers.instructions_handlers import main_instructions_router
from src.logic.bot_logic.handlers.profile_handlers import main_profile_router
from src.logic.bot_logic.handlers.projects_handlers import main_projects_router
from src.logic.bot_logic.handlers.service_handlers import main_service_router

routes = [
    main_service_router,
    common_router,
    main_admin_router,
    main_projects_router,
    main_profile_router,
    main_instructions_router,
]

handlers_router = Router()
for _ in routes:
    handlers_router.include_router(_)
