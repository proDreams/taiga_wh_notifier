from src.core.settings import Configuration
from src.logic.bot_logic.handlers import handlers_router


async def register_routers():
    Configuration.dispatcher.include_router(handlers_router)
