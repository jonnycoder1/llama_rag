from functools import wraps
from icecream import ic
import logging
import time


def get_logger(name):
    """
    Create and return a logger with the given name.
    """
    filename = name.split('/')[-1]
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


logger = get_logger(__file__)
ic.configureOutput(includeContext=True,
                   outputFunction=lambda s: logger.info(s))


def timer(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        logger.info(f"{func.__name__} took {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer
