import logging
from functools import wraps
from time import time

logger = logging.getLogger('runtime')


def runtime(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time()
        f = func(self, *args, **kwargs)
        runtime = time() - start
        if runtime > 0.1:
            logger.info(f'func:{func.__name__}, runtime:{round(time() - start, 2)}')
        else:
            logger.debug(f'func:{func.__name__}, runtime:{round(time() - start, 2)}')
        return f
    return wrapper

