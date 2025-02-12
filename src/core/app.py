import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.settings import Configuration
from src.entities.enums.environment_enum import EnvironmentEnum


@asynccontextmanager
async def prod_lifespan(app: FastAPI):
    url_webhook = f"{Configuration.settings.WEBHOOK_DOMAIN}{Configuration.settings.UPDATES_PATH}"
    await Configuration.bot.set_webhook(
        url=url_webhook,
        allowed_updates=Configuration.dispatcher.resolve_used_update_types(),
        drop_pending_updates=True,
    )

    yield

    await Configuration.bot.delete_webhook()
    await Configuration.bot.session.close()


@asynccontextmanager
async def dev_lifespan(app: FastAPI):
    async def _start_polling():
        await Configuration.dispatcher.start_polling(Configuration.bot, handle_signals=False)

    polling_task = asyncio.create_task(_start_polling())

    yield

    polling_task.cancel()
    await Configuration.bot.session.close()


def run_app():
    match Configuration.settings.current_env:
        case EnvironmentEnum.prod:
            web_app = FastAPI(lifespan=prod_lifespan)
        case _:  # EnvironmentEnum.dev | EnvironmentEnum.test
            web_app = FastAPI(lifespan=dev_lifespan)

    uvicorn.run(web_app, host="0.0.0.0", port=8000, loop="asyncio", log_config=None)
