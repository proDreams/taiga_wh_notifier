from logging import Logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dynaconf import Dynaconf

from src.core.Base.singleton import Singleton
from src.utils.logger_utils import LoggerUtils
from src.utils.yaml_utils import generate_strings_dict


class Configuration(Singleton):
    """
    Singleton implementation for managing application configuration.
    """

    settings = Dynaconf(envvar_prefix=False, environments=True, settings_files=["config/settings.yaml"])
    logger = LoggerUtils(settings=settings)
    strings = generate_strings_dict(path=settings.YAML_FILE_PATH)
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dispatcher = Dispatcher()


def get_settings() -> Dynaconf:
    """
    Returns the current settings configuration.

    :return: The settings configuration object.
    :rtype: Dynaconf
    """
    return Configuration.settings


def get_strings() -> dict:
    """
    Returns the dictionary containing string configurations.

    :returns: A dictionary with configuration strings.
    :rtype: dict
    """
    return Configuration.strings


def get_logger(**kwargs) -> Logger:
    """
    Returns a logger instance based on the provided configuration.

    :param kwargs: Arbitrary keyword arguments passed to the logging library.
    :type kwargs: dict
    :returns: Logger instance configured according to the provided parameters.
    :rtype: Logger
    """
    return Configuration.logger.get_logger(**kwargs)
