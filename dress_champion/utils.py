import sys
import logging


def configure_logger(logger, level):
    """Configure logger to output to stream and set level."""
    stream = logging.StreamHandler(stream=sys.stdout)
    stream.level = level
    logger.handlers = []
    logger.addHandler(stream)
    logger.level = level
