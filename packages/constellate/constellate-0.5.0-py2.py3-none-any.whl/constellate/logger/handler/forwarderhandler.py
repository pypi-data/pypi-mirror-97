import logging


class LoggerProxyHandler(logging.Handler):
    def __init__(self, target_logger: logging.Logger = None):
        self._target_logger = target_logger

    def emit(self, record: logging.LogRecord) -> None:
        if self._target_logger is not None and self._target_logger.isEnabledFor(record.levelno):
            self._target_logger.handle(record)
