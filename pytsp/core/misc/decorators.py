
from functools import wraps


def cached(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, 'cache'):
            setattr(wrapper, 'cache', method(*args, **kwargs))

        return wrapper.cache

    return wrapper
