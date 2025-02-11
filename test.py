from src.core.settings import Configuration

logger = Configuration.logger.get_logger(name=__name__)


def main():
    logger.info("Hello, world!")


main()
