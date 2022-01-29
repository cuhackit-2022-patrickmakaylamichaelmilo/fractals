import traceback
import logging


def format_exception(e: Exception) -> str:
    return "".join(traceback.format_exception(type(e), e, e.__traceback__, 4))


def log_exception(e: Exception, logger: logging.Logger) -> None:
    """Logs a nicely formatted exception"""

    traceback_lines = format_exception(e).strip("\n").split("\n")

    for line in traceback_lines:
        logger.error(line)
