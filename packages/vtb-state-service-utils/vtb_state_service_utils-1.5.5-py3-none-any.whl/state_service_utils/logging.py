import logging.handlers
import os

from vtb_py_logging import OrderJsonFormatter, OrderConsoleFormatter

from .exceptions import StateServiceException

APP_NAME = os.getenv('APP_NAME', 'app')

if not APP_NAME and not os.getenv('DEBUG'):
    raise StateServiceException('Configuration error, APP_NAME required')

LOG_DIR_PATH = f'/var/log/{APP_NAME}'
os.makedirs(LOG_DIR_PATH, exist_ok=True)

LOG_FILE_NAME = f'{APP_NAME}.log'


def create_logger():
    logger = logging.getLogger(APP_NAME)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(OrderConsoleFormatter())

    jh = logging.handlers.TimedRotatingFileHandler(when='H', interval=1, backupCount=1,
                                                   filename=f'{LOG_DIR_PATH}/{LOG_FILE_NAME}')
    jh.setLevel(logging.INFO)
    jh.setFormatter(OrderJsonFormatter())

    logger.addHandler(ch)
    logger.addHandler(jh)
    return logger


logger = create_logger() if not logging.getLogger(APP_NAME).hasHandlers() else logging.getLogger(APP_NAME)
