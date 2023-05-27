import logging
import logging.handlers
import sys


class Logger:

    def __init__(self, config) -> None:
        self.logger_level = logging.getLevelName(config.logger["level"])
        self._setup_python_logger()

    def _setup_python_logger(self) -> None:
        log_formatter = logging.Formatter(
            "%(asctime)s [%(filename)-12.12s:%(lineno)-2.4s] [%(levelname)-5.7s]  %(message)s")
        self.logger = logging.getLogger()
        self.logger.setLevel(self.logger_level)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        self.logger.addHandler(console_handler)

    def message(self, message: str, severity: str) -> None:
        logger_level = logging.getLevelName(severity)
        if logger_level < self.logger_level:
            return

        self.logger.log(level=logger_level, msg=message)

    def debug(self, message: str) -> None:
        self.message(message, "DEBUG")

    def info(self, message: str) -> None:
        self.message(message, "INFO")

    def warning(self, message: str) -> None:
        self.message(message, "WARNING")

    def error(self, message: str) -> None:
        self.message(message, "ERROR")
