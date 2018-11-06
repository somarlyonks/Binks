# Outputs Record

## local script try & retry tests

```stdout
(binks) > scripts/local.py
[BINKS]: Date: Tue Nov  6 11:59:40 2018
[BINKS]: Downloading image - https://www.bing.com/az/hprichbg/rb/AutumnNeuschwanstein_EN-CN10604288553_1920x1080.jpg
[BINKS]: Error - wrong response for https://www.bing.com/az/hprichbg/rb/AutumnNeuschwanstein_EN-CN10604288553_1920x1080.jpg
[BINKS]: Retrying the failed tasks.
[BINKS]: Downloading image - https://www.bing.com/az/hprichbg/rb/AutumnNeuschwanstein_EN-CN10604288553_1920x1080.jpg
[BINKS]: Error - wrong response for https://www.bing.com/az/hprichbg/rb/AutumnNeuschwanstein_EN-CN10604288553_1920x1080.jpg
[BINKS]: Done. Total: 1  Failed: 1
(binks) > scripts/local.py
[BINKS]: Date: Tue Nov  6 11:59:57 2018
[BINKS]: Downloading image - https://www.bing.com/az/hprichbg/rb/AutumnNeuschwanstein_EN-CN10604288553_1920x1080.jpg
[BINKS]: Done. Total: 1  Failed: 0
(binks) > scripts/local.py
[BINKS]: Date: Tue Nov  6 12:00:00 2018
[BINKS]: Downloading image - https://www.bing.com/az/hprichbg/rb/AutumnNeuschwanstein_EN-CN10604288553_1920x1080.jpg
[BINKS]: Image exists - /home/sy/Desktop/AutumnNeuschwanstein.jpg
[BINKS]: Done. Total: 1  Failed: 0
```