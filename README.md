# Binks

A script for downloading bing desktops. @see [LOCAL](##LOCAL)

Or you can install the dropbox app. @see [APP](##APP)

## LOCAL

Currently you can register a schedule with _crontab_. like;

`0 11 * * * /home/sy/Devel/Binks/scripts/local.py`

### Configs with environment variables

__BINKS_LOCAL_PERIOD__ : Period of the script (runs every _???_ days), default: `1`

__BINKS_LOCAL_PATH__ : Path to save images, default: `/srv/Binks/local`

__BINKS_LOCAL_TIMEOUT__ : Timeout of trying connect, default: `5`

## APP

TODO

## DEV

### python3.7.0b2

With pyenv and virtualenvwrapper

```shell
pyenv install 3.7.0b2
mkvirtualenv binks --python=/home/sy/.pyenv/versions/3.7.0b2/bin/python3.7
pip install -r requirements.txt
```
