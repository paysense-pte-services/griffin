import logging
import time

LOGGER = logging.getLogger("griffin_decorators")


def singleton(cls):
    """
    This decorator make sure that there is only 1 instance of the class.
    Args:
        cls:
    Returns:
    """
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


def timed(method):
    def _timed(*args, **kwargs):
        ts = time.time()
        result = method(*args, **kwargs)
        te = time.time()
        LOGGER.info("({}.{}) took {:.2f}s".format(
            method.__module__, method.__name__, te - ts))
        return result
    return _timed
