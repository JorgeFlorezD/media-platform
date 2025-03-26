import logging
import sys

import structlog
from structlog.contextvars import merge_contextvars


class Log:
    logger: logging.Logger = logging.getLogger()

    @staticmethod
    def setup_logging(log_level: int, title: str):
        logger = logging.getLogger(title)
        logger.setLevel(log_level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        logger.addHandler(handler)

        structlog.configure(
            processors=[
                merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
        )
        Log.logger = structlog.get_logger(title)
        return Log.logger
