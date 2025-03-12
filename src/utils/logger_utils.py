import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import dynaconf

from src.core.Base.singleton import Singleton


class LoggerUtils(Singleton):
    def __init__(self, settings: dynaconf.Dynaconf):
        self.log_dir = Path(settings.LOG_DIR)
        self.log_file = self.log_dir / settings.LOG_FILE
        self.log_level = settings.LOG_LEVEL
        self.max_log_size = settings.MAX_SIZE_MB
        self.backup_count = settings.BACKUP_COUNT
        self.pre_registered_loggers = settings.PRE_REGISTERED_LOGGERS

        self._setup_logging_directory()

        for logger_name in self.pre_registered_loggers:
            self.get_logger(logger_name)

    def _setup_logging_directory(self):
        """
        Sets up the logging directory.

        This method ensures that the directory specified by `self.log_dir` exists.
        If the directory already exists or cannot be created due to permissions issues,
        it handles these cases gracefully without raising an exception.

        :returns: True if the directory was successfully created or already existed; False otherwise.
        :rtype: bool
        """
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def _get_console_handler(self) -> logging.Handler:
        """
        Returns a logging handler for the console.

        :returns: A new logging handler configured to log to the console.
        :rtype: logging.Handler
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self.get_log_formatter())
        return console_handler

    def _get_file_handler(self) -> logging.Handler:
        """
        Retrieves a rotating file handler for logging.

        :returns: A logging handler that writes logs to a rotating file.
        :rtype: logging.Handler
        """
        file_handler = RotatingFileHandler(
            filename=self.log_file,
            encoding="utf-8",
            maxBytes=self.max_log_size * 1024 * 1024,
            backupCount=self.backup_count,
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.get_log_formatter())
        return file_handler

    @staticmethod
    def get_log_formatter() -> logging.Formatter:
        """
        Returns a logging formatter with a specific format for log messages.

        This formatter includes the following information in each log message:
        - The timestamp (asctime)
        - The logging level (levelname)
        - The name of the logger (name)
        - The filename where the log record was created (filename)
        - The function name where the log record was created (funcName)
        - The line number where the log record was created (lineno)
        - The actual log message (message)

        :returns: A logging formatter instance with the specified format.
        :rtype: logging.Formatter
        """
        return logging.Formatter(
            fmt="[%(asctime)-25s][%(levelname)-8s][%(name)-35s]"
            "[%(filename)-20s][%(funcName)-25s][%(lineno)-5d][%(message)s]"
        )

    def get_logger(self, name: str | None = None) -> logging.Logger:
        """
        Returns a logger instance with the specified name.

        :param name: The name of the logger. If None, the root logger is returned.
        :type name: str | None

        :returns: A logger instance configured with handlers and logging level.
        :rtype: logging.Logger
        :raises ValueError: If the specified logging directory could not be set up.
        """

        logger = logging.getLogger(name)

        if not logger.hasHandlers():
            logger.setLevel(self.log_level)
            logger.addHandler(self._get_console_handler())
            logger.addHandler(self._get_file_handler())

        return logger
