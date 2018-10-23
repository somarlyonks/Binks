
import time
import contextlib
import sys
import inspect
import os
import types
from functools import wraps

import requests as q


PROTOCOL = 'https'
HOST_URL = f'{PROTOCOL}://www.bing.com'
TIMEOUT = 5


def main(fn):
    locale = inspect.stack()[1][0].f_locals
    module = locale.get("__name__", None)
    if module == '__main__':
        locale[module] = fn
        args = sys.argv[1:]
        fn(*args)
    return fn


def q_get(url):
    r = q.get(HOST_URL + url, timeout=TIMEOUT)
    try:
        r.raise_for_status()
    except q.HTTPError:
        return print(f'[BING]: Error - wrong response for {HOST_URL + url}')
    return r


@contextlib.contextmanager
def stopwatch(message):
    t = time.time()
    try:
        yield
    finally:
        print('[DROPBOX]: Total elapsed time for %s: %.3f' % (message, time.time() - t))


ENV_NAME = 'https_proxy'


class Proxy(object):
    """
    Usage
    ```python
    with Proxy('https://127.0.0.1:8123'):
        pass
    ```
    or
    ```python
    @Proxy('https://127.0.0.1:8123')
    def func(x):
        pass
    ```
    or
    ```python
    class Cls(object):
        https_proxy = 'https://127.0.0.1:8123'

        @Proxy
        def method(self):
            pass
    ```
    TODO
      as cls decorator (has to rewrite the __new__)
    """
    def __init__(self, target):
        self.location = getattr(target, ENV_NAME, target)
        if type(self.location) is not str:
            wraps(target)(self)
            # self.__call__(target)

    def __enter__(self):
        self.former = os.getenv(ENV_NAME)
        os.environ[ENV_NAME] = self.location
        print('[BINKS]: Under proxy - ', self.location)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('[BINKS]: Exit proxy.')
        del os.environ[ENV_NAME]
        if self.former:
            os.environ[ENV_NAME] = self.former

    def __call__(self, *args, **kwargs):
        target = args[0]

        @wraps(target)
        def wrapper(*args, **kwargs):
            with self:
                return target(*args, **kwargs)

        if type(self.location) is not str:
            self.location = getattr(target, ENV_NAME, target)
            if type(self.location) is not str:
                raise AttributeError(f'[PROXY]: target or target.{ENV_NAME} is supposed to be str.')

        if getattr(self, '__wrapped__', None):
            with self:
                return self.__wrapped__(*args, **kwargs)  # pylint: disable=E1101
        else:
            return wrapper

    def __get__(self, inst, cls):
        return self if inst is None else types.MethodType(self, inst)
