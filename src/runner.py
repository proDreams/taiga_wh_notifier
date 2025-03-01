from src.core.app import run_app
from src.core.settings import get_logger

logger = get_logger(name=__name__)


def run():
    logger.info("Starting...")
    run_app()
    logger.info("Stopping...")
