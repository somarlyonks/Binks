# Binks

A script for downloading bing desktops. @see [LOCAL](##LOCAL)

Or you can install the dropbox app. @see [APP](##APP)

## LOCAL

Currently you can register a daily schedule with crontab. like;

`0 11 * * * /home/sy/.virtualenvs/binks/bin/python /home/sy/Devel/Binks/scripts/local.py`

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
