#

from worker import BinksWorker
from utils import main


clients_pool = []  # get it from db server


@main
def pooling():
    for client in clients_pool:
        try:
            dbx = BinksWorker(client)
            dbx.binks_work()
        except Exception:
            pass
