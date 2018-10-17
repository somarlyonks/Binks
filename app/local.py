"""
The local verison for personal.
TODO
  send email to ask for saving
  customize daily/weekly
  context of dropbox
  more flexible proxy
  makefile/argparse [--proxy=]
"""


import json
import os
import sys

import dropbox

from utils import q_get, main, stopwatch, HOST_URL


API = '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US&ensearch=1'
PROXY = 'http://localhost:8123'
DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN', '')
try:
    DBX = dropbox.Dropbox(DROPBOX_TOKEN)
except AssertionError as err:
    print('[DROPBOX]: DROPBOX_TOKEN is not found in environment, exited: 1')
    sys.exit(1)


def upload(dbx, data, name, overwrite=False):
    path = 'bing/buffer'
    mode = (dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add)

    with stopwatch('uploading %d bytes' % len(data)):
        try:
            res = dbx.files_upload(data, path, mode, mute=True)
        except dropbox.exceptions.ApiError as err:
            return print('[DORPBOX]: API error - ', err)
    print('[DROPBOX]: uploaded as', res.name.encode('utf8'))
    return res


def download(url):
    print(f'[BING]: Downloading image - {HOST_URL + url}')
    if not url.endswith('.jpg'):
        return print(f'[BING]: Error - wrong extension name.')

    name = url.split('/')[-1]
    data = q_get(url)
    upload(DBX, data.content, name)


@main
def _():
    os.environ['https_proxy'] = PROXY
    r = q_get(API)
    j = json.loads(r and r.text or '{}')
    for img in j.get('images', []):
        download(img.get('url', ''))
