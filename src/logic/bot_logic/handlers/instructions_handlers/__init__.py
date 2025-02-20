from aiogram import Router

from src.logic.bot_logic.handlers.instructions_handlers.instructions_handlers import instructions_router

main_instructions_router = Router()
main_instructions_router.include_routers(instructions_router)
