# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ghost']
entry_points = \
{'web.apps': ['ghost = ghost:app']}

setup_kwargs = {
    'name': 'ghost-in-the-machine',
    'version': '0.0.2a0',
    'description': 'Host web applications.',
    'long_description': '# ghost\nserve a web [application](https://github.com/angelogladding/web#a-simple-application) at a domain\n\n**Linux:** `wget gh.ost.lol/ghost.py -qO ghost && python3 ghost`  \n**OSX:** `curl gh.ost.lol/ghost.py ghost && python3 ghost`\n\n**Hosts:** [Digital Ocean](https://cloud.digitalocean.com/account/api/tokens)  \n**Registrars:** [Dynadot](https://www.dynadot.com/account/domain/setting/api.html)\n\n    $ wget gh.ost.lol/ghost.py -qO ghost && time python3 ghost\n    presence name: testing\n    digital ocean token:\n\n    creating droplet\n    spawning sudoer ghost\n\n     0:00 updating, upgrading\n     0:33 installing build-essential, expect, psmisc, xz-utils, zip,\n            git, fcgiwrap, supervisor, redis-server, haveged, libicu-dev,\n            python3-icu, libsqlite3-dev, libssl-dev, libffi-dev, zlib1g-dev,\n            python3-dev, python3-crypto, python3-libtorrent, ffmpeg,\n            libsm-dev, python-opencv, libevent-dev, pandoc, graphviz,\n            libgtk-3-0, libdbus-glib-1-2, xvfb, x11-utils, libenchant-dev,\n            ufw, tmux, php-curl, php-fpm, php-gd, php-intl, php-mbstring,\n            php-mysql, php-soap, php-xml, php-xmlrpc, php-zip\n     3:27 installing python-3.9.0\n     3:27   downloading, extracting, configuring\n     4:00   making\n     7:40   installing\n     8:23 creating virtual environment\n     8:29   installing SQLite-latest\n    10:19   installing Ghost ecosystem\n    10:19     src\n    10:43     term\n    10:47     kv\n    10:53     sql\n    10:57     web\n    12:22     ghost\n    12:27 installing nginx-1.18.0\n    12:27   downloading, extracting, configuring\n    12:36   making\n    13:38   installing\n    13:38   generating a large prime for TLS (this will take a long time)\n\n    You may now sign in to your host while installation continues:\n        https://165.227.30.1?secret=sepkpt\n\n    13:42 installing tor-0.4.4.5\n    13:42   downloading, extracting, configuring\n    14:10   making\n    21:12   installing\n    21:13 installing firefox-82.0\n    21:29 installing geckodriver-0.27.0\n\n    python3 ghost ... 22:25.14 total\n\n![](https://github.com/angelogladding/ghost/raw/main/interface.png)\n',
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
