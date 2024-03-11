import logging
import sys

from config.env import LOG_LEVEL


def prepare_logger():
    logger = logging.getLogger()
    logger.setLevel(level=LOG_LEVEL)
    formatter = logging.Formatter(
        "%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s"
    )
    if not logger.handlers:
        lh = logging.StreamHandler(sys.stdout)
        lh.setFormatter(formatter)
        logger.addHandler(lh)
    return logger
