
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


def log(*msg):
    print(*msg, qget())


proxy = Proxy(PROXY)


@main
def f():
    class C(object):
        def __init__(self, x):
            self.x = x
            self.https_proxy = PROXY

        @Proxy
        def gp(self, y=1):
            log('inst', self.x, y)

        @proxy
        def gp2(self, y=2):
            log('inst', self.x, y)

        def g(self):
            log('inst', 'it should timeout:')

    c = C(1)
    c.gp()
    c.gp2()
    c.g()

    with proxy:
        with proxy:
            log('with')

    c.g()

    @proxy
    def gp3():
        log('func')

    gp3()
