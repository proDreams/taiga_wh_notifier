import logging
import os

from src.core.const import LOG_FILE_PATH


def clear_log_file(log_file_path: str):
    """
    Очищает содержимое файла логов.

    :param log_file_path: Путь к файлу логов, который нужно очистить.
    :type log_file_path: str
    """
    temp_logger = logging.getLogger("temp_logger")
    temp_logger.setLevel(logging.INFO)
    temp_logger.addHandler(logging.StreamHandler())

    if os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.write("")
        temp_logger.debug(f"Файл {log_file_path} успешно очищен.")


def create_log_handlers(log_file_path: str):
    """
    Создаёт обработчики для логгера.
    :param log_file_path: Путь к файлу логов.
    :return: Список обработчиков.
    """
    file_handler = logging.FileHandler(log_file_path)
    stream_handler = logging.StreamHandler()
    return [file_handler, stream_handler]


def setup_logger():
    """
    Настраивает логгер для приложения.
    """
    clear_log_file(LOG_FILE_PATH)

    logging.basicConfig(
        # Необходимо скорректировать логику таким образом, чтобы динамически ссылаться на уровень логирования из
        # раннера или Dockerfile (что мне кажется логичнее)
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        # Расположение `LOG_FILE_PATH` сейчас находится в CORE, но предполагаю, что ты захочешь переместить в другое
        # место
        handlers=create_log_handlers(LOG_FILE_PATH),
    )

    return logging.getLogger(__name__)


# Не понимаю как в твоей структуре правильно определить экземпляр логгера. Тут или где-то в `core`, поэтому пока оставлю
# тут
logger = setup_logger()
