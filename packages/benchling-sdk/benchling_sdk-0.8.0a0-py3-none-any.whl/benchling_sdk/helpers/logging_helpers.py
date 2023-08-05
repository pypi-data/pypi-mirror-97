import logging


def default_logger(name: str = "benchling_sdk") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.addHandler(logging.NullHandler())
    return logger


sdk_logger = default_logger()
