import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.settings import Configuration, get_settings
from src.entities.enums.environment_enum import EnvironmentEnum
from src.infrastructure.database.mongo_dependency import MongoDBDependency
from src.logic.bot_logic.handlers.service_handlers.service_events_handlers import (
    start_bot,
    stop_bot,
)
from src.logic.web_app_logic.exception_handler import handling_exceptions
from src.presentation.bot_routers.init_router import (
    register_bot_middlewares,
    register_bot_routers,
)
from src.presentation.web_app_routes import web_app_router


@asynccontextmanager
async def prod_lifespan(app: FastAPI):
    settings = get_settings()
    bot = Configuration.bot

    url_webhook = f"{settings.WEBHOOK_DOMAIN}{settings.UPDATES_PATH}"
    await bot.set_webhook(
        url=url_webhook,
        allowed_updates=Configuration.dispatcher.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    await start_bot()

    yield

    MongoDBDependency().close()

    await stop_bot()

    await bot.delete_webhook()
    await bot.session.close()


@asynccontextmanager
async def dev_lifespan(app: FastAPI):
    async def _start_polling():
        await Configuration.dispatcher.start_polling(Configuration.bot, handle_signals=False)

    polling_task = asyncio.create_task(_start_polling())

    yield

    MongoDBDependency().close()

    polling_task.cancel()
    await Configuration.bot.session.close()


def run_app():
    match current_env := get_settings().current_env:
        case EnvironmentEnum.PROD:
            web_app = FastAPI(lifespan=prod_lifespan)
        case EnvironmentEnum.DEV | EnvironmentEnum.TEST:
            web_app = FastAPI(lifespan=dev_lifespan)
        case _:
            raise RuntimeError(f"Unknown environment {current_env}")

    asyncio.run(register_bot_middlewares())
    asyncio.run(register_bot_routers())
    web_app = asyncio.run(handling_exceptions(app=web_app))
    web_app.include_router(web_app_router)
    uvicorn.run(web_app, host="0.0.0.0", port=8000, loop="asyncio", log_config=None)
