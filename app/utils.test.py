
import requests as q

from utils import Proxy, main


PROXY = 'http://127.0.0.1:8123'
HOST = 'https://google.com'
TIMEOUT = 5


def qget():
    try:
        return q.get(HOST, timeout=TIMEOUT).status_code
    except q.ConnectionError:
        return 'timeout'


def log(msg):
    print(msg, qget())


@main
def f():
    class C(object):
        def __init__(self, x):
            self.x = x
            self.https_proxy = 'http://127.0.0.1:8123'

        @Proxy
        def gp(self):
            log('inst')

        def g(self):
            log('inst')

    c = C(1)
    c.gp()
    c.g()  # make sure this will timeout

    proxy = Proxy(PROXY)

    with proxy:
        log('with')

    @proxy
    def gp2():
        log('func')

    gp2()
