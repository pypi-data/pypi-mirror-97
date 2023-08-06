import logging
from typing import Dict

__LOGGERS: Dict[str, logging.Logger] = dict()
CRITICAL = logging.CRITICAL  # 50
ERROR = logging.ERROR  # 40
WARNING = logging.WARNING  # 30
INFO = logging.INFO  # 20
DEBUG = logging.DEBUG  # 10
NOTSET = logging.NOTSET  # 0


def get_logger(
    name,
    level=logging.INFO,
):
    if name not in __LOGGERS:
        logger = logging.getLogger(name)
        logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        __LOGGERS[name] = logger
    return __LOGGERS[name]
