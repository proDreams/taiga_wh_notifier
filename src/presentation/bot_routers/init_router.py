from src.core.settings import Configuration
from src.logic.bot_logic.handlers import handlers_router
from src.logic.bot_logic.middlewares.dependency_middleware import DependencyMiddleware


async def register_bot_routers() -> None:
    """
    Registers bot routers with the application dispatcher.
    """
    Configuration.dispatcher.include_router(handlers_router)


async def register_bot_middlewares() -> None:
    """
    Register bot middlewares for the application.

    This method updates the dispatcher's middleware with an instance of UserMiddleware.
    """
    Configuration.dispatcher.update.middleware(DependencyMiddleware())
