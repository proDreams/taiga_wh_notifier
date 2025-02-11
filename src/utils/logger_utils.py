# import logging
# from logging.handlers import RotatingFileHandler
# from pathlib import Path
# from dynaconf import Dynaconf
#
#
# class LoggerUtils:
#     def __init__(self):
#         self.log_dir = Path(settings.logging.dir)
#         self.log_file = self.log_dir / settings.logging.file
#         self.log_level = getattr(logging, settings.logging.level, logging.INFO)
#         self.max_log_size = settings.logging.max_size
#         self.backup_count = settings.logging.backup_count
#
#         self._setup_logging_directory()
#
#     def setup_logging_directory(self):
#         """Создаёт папку для логов, если её нет."""
#         self.log_dir.mkdir(parents=True, exist_ok=True)
#
#
#     def get_console_handler(self) -> logging.Handler:
#         """Создаёт обработчик логов для консоли."""
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(LOG_LEVEL)
#         console_handler.setFormatter(get_log_formatter())
#         return console_handler
#
#
#     def get_file_handler() -> logging.Handler:
#         """Создаёт обработчик логов для файла с ротацией."""
#         file_handler = RotatingFileHandler(
#             filename=LOG_FILE,
#             encoding="utf-8",
#             maxBytes=MAX_SIZE,
#             backupCount=BACKUP_COUNT
#         )
#         file_handler.setLevel(LOG_LEVEL)
#         file_handler.setFormatter(get_log_formatter())
#         return file_handler
#
#
#     def get_log_formatter() -> logging.Formatter:
#         """Возвращает форматтер для логов."""
#         return logging.Formatter(
#             fmt="%(asctime)s - [%(levelname)s] - %(name)s - "
#                 "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
#         )
#
#
#     def get_logger(name: str | None = None) -> logging.Logger:
#         """
#         Возвращает настроенный логгер.
#
#         :param name: __name__ файла, вызывающего логгер
#         :return: Объект логгера
#         """
#         setup_logging_directory()
#
#         logger = logging.getLogger(name)
#
#         if not logger.hasHandlers():
#             logger.setLevel(LOG_LEVEL)
#             logger.addHandler(get_console_handler())
#             logger.addHandler(get_file_handler())
#
#         return
#
