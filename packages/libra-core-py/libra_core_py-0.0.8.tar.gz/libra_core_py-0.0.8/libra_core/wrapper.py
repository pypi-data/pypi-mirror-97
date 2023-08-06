import functools
from .log import log_exception


def try_catch_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            log_exception(ex)
            return None

    return wrapper


def catch_raise_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            log_exception(ex)
            raise ex

    return wrapper
