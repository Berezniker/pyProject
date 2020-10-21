from functools import wraps
from typing import Callable


def cached(func: Callable):
    """
    Remembers the last returned value of the function <func>
    and allows you to return it again in O(1) when called with key "cache"

    :param func: decorated function
    :return: wrapper
    """
    return_value = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal return_value
        if kwargs.get("cache") is None:
            return_value = func(*args, **kwargs)
        return return_value

    return wrapper
