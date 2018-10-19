
import time
import contextlib
import sys
import inspect

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


def https_proxy(f):
    """TODO"""
    pass
