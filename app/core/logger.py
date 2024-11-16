from loguru import logger
import sys


class Logger:
    def __init__(self, log_file: str = "app.log"):
        self.log_file: str = log_file
        self._configure_logger()

    def _configure_logger(self):
        logger.remove()

        logger.add(self.log_file, level="DEBUG", rotation="100 MB", compression="zip")

        logger.add(sys.stderr, level="INFO", colorize=True)

    def get_logger(self):
        return logger


logger_instance = Logger()
