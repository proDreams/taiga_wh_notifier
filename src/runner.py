from time import sleep

from src.core.settings import Configuration

logger = Configuration.logger.get_logger(name=__name__)


def run():
    logger.info("Starting...")
    sleep(10)
    logger.info("Stopping...")
