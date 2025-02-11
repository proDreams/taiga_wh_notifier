import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from unittest import TestCase

from src.core.settings import Configuration
from src.utils.logger_utils import LoggerUtils


class TestLoggerClass(TestCase):
    target_class = LoggerUtils
    settings = Configuration.settings

    def test_single_instance(self) -> None:
        """
        Ensures that a class has only one instance.

        :raises: AssertionError: If multiple instances of the target class are actually
        """
        instance1 = self.target_class(self.settings)
        instance2 = self.target_class(self.settings)
        assert instance1 is instance2, "Instance1 should be equal to instance2"

    def test_logging_directory(self):
        """
        Tests the `_setup_logging_directory()` method.

        This test ensures that:
        1. The method successfully creates the logging directory.
        2. The directory exists after execution.
        3. The directory is recognized as a valid directory.

        :raises ValueError: If the provided settings dictionary does not contain the necessary configuration.
        """
        logger = self.target_class(self.settings)
        temp_log_dir = Path("tests/configuration/fixtures/logs")
        logger.log_dir = temp_log_dir

        logger._setup_logging_directory()

        assert temp_log_dir.exists()
        assert temp_log_dir.is_dir()

    def test_get_console_handler(self) -> None:
        """
        Tests the `_get_console_handler()` method.

        This test verifies that:
        1. The method returns a `StreamHandler` instance.
        2. The handler's log level matches the logger's configured log level.
        3. The handler has a formatter, and its format matches the expected format.

        :param self: Instance of the test class.
        """
        logger = self.target_class(self.settings)
        console_handler = logger._get_console_handler()

        assert isinstance(console_handler, logging.StreamHandler)

        expected_level = getattr(logging, logger.log_level, logging.INFO)
        assert console_handler.level == expected_level
        assert console_handler.formatter is not None
        assert console_handler.formatter._fmt == logger.get_log_formatter()._fmt

    def test_get_file_handler(self) -> None:
        """
        Tests `_get_file_handler()` to ensure correct configuration.

        Verifies:
        - The handler is an instance of `RotatingFileHandler`.
        - The log file name is correct.
        - The max log size and backup count match the logger's configuration.
        """
        logger = self.target_class(self.settings)
        expected_max_bytes = self.settings.MAX_SIZE_MB * 1024 * 1024
        expected_backup_count = self.settings.BACKUP_COUNT
        logger.max_log_size = self.settings.MAX_SIZE_MB
        logger.backup_count = self.settings.BACKUP_COUNT

        file_handler = logger._get_file_handler()

        assert isinstance(file_handler, RotatingFileHandler)
        assert Path(file_handler.baseFilename).name == "logs.txt"
        assert file_handler.maxBytes == expected_max_bytes
        assert file_handler.backupCount == expected_backup_count

    def test_get_log_formatter(self) -> None:
        """
        Tests the `get_log_formatter()` to ensure correct formatter.

        :param None: No parameters are expected.
        :return: This method does not return a value.
        :rtype: None

        This test checks if the get_log_formatter method returns an instance of logging.Formatter.
        It also verifies that the format string returned by the formatter matches the expected log format.
        """
        formatter = LoggerUtils.get_log_formatter()
        assert isinstance(formatter, logging.Formatter)
        expected_format = "%(asctime)s - [%(levelname)s] - %(name)s - ("
        expected_format += "%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
        assert formatter._fmt == expected_format
