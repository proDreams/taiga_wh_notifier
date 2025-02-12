from src.core.app import run_app
from src.core.settings import Configuration

logger = Configuration.logger.get_logger(name=__name__)


def run():
    logger.info("Starting...")
    run_app()
    logger.info("Stopping...")
