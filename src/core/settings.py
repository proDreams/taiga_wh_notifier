from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dynaconf import Dynaconf

from src.core.Base.singleton import Singleton
from src.utils.logger_utils import LoggerUtils
from src.utils.yaml_utils import get_strings


class Configuration(Singleton):
    """
    Singleton implementation for managing application configuration.

    :ivar settings: Dynamic configuration object for loading and accessing settings from a YAML file.
    :type settings: Dynaconf
    """

    settings = Dynaconf(envvar_prefix=False, environments=True, settings_files=["config/settings.yaml"])
    logger = LoggerUtils(settings=settings)
    strings = get_strings(path=settings.YAML_FILE_PATH)
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dispatcher = Dispatcher()
