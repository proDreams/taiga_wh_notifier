from src.core.settings import Configuration
from src.logic.bot_logic.handlers import handlers_router
from src.logic.bot_logic.middlewares.user_middleware import UserMiddleware


async def register_bot_routers() -> None:
    Configuration.dispatcher.include_router(handlers_router)


async def register_bot_middlewares() -> None:
    Configuration.dispatcher.update.middleware(UserMiddleware())
