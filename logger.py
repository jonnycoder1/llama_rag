from functools import wraps
from icecream import ic, install
import logging
import time

# Set logging level to your liking
LOG_LEVEL = logging.INFO


def get_logger():
    """
    Create and return a logger
    """
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = get_logger()

# Configure icecream & redirect output to logger.info
ic.configureOutput(includeContext=True,
                   outputFunction=lambda s: logger.info(s))

# Installing icecream makes `ic()` available to all files without needing import
install()


def timer(func):
    """
    Create and return a decorator for measuring times
    """
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        logger.info(f"{func.__name__} took {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer
