import os
import sys

import logging


def get_basic_stdout_logger(log_level: str = None) -> logging.Logger:
    if not log_level:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    # Convert the log level to an integer
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    # Set the log level, force to STDOUT
    logging.basicConfig(
        stream=sys.stdout,
        level=numeric_level,
        format="%(levelname)s:     %(asctime)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger
