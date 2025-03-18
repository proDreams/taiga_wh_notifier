from logging import Logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dynaconf import Dynaconf
from dynaconf.validator import Validator

from src.core.Base.singleton import Singleton
from src.utils.logger_utils import LoggerUtils
from src.utils.yaml_utils import generate_strings_dict


class Configuration(Singleton):
    """
    Singleton implementation for managing application configuration.
    """

    settings = Dynaconf(
        envvar_prefix=False,
        environments=True,
        settings_files=["config/settings.yaml"],
        validators=[
            Validator("ADMIN_IDS", must_exist=True),
            Validator("ERRORS_CHAT_ID", must_exist=True),
            Validator("UPDATES_PATH", default="/updates"),
            Validator("WEBHOOK_DOMAIN", must_exist=True),
            Validator("YAML_FILE_PATH", default="strings"),
            Validator("LOG_DIR", default="logs"),
            Validator("LOG_FILE", default="logs.txt"),
            Validator("LOG_LEVEL", default="INFO"),
            Validator("MAX_SIZE_MB", default=10),
            Validator("BACKUP_COUNT", default=5),
            Validator("PRE_REGISTERED_LOGGERS", default=["uvicorn", "aiogram"]),
            Validator("DEFAULT_LANGUAGE", default="ru"),
            Validator("ALLOWED_LANGUAGES", default=["ru", "en"]),
            Validator("ITEMS_PER_PAGE", default=5),
            Validator("TIMESTAMP_FORMAT", default="%H:%M %d.%m.%Y"),
            Validator("TIME_ZONE", default="Europe/Moscow"),
            Validator("TRUNCATED_STRING_LENGTH", default=100),
            Validator("TELEGRAM_BOT_TOKEN", must_exist=True),
            Validator("DB_URL", must_exist=True),
            Validator("DB_NAME", default="taigram"),
            Validator("REDIS_URL", default="redis://redis:6379/0"),
            Validator("REDIS_MAX_CONNECTIONS", default=20),
        ],
    )
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
    if not kwargs.get("name"):
        kwargs["name"] = __name__

    return Configuration.logger.get_logger(**kwargs)
