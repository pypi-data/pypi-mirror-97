# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ghost']
install_requires = \
['understory>=0.0.1,<0.0.2']

entry_points = \
{'web.apps': ['ghost = ghost:app']}

setup_kwargs = {
    'name': 'ghost-in-the-machine',
    'version': '0.0.19',
    'description': 'Manage your digital presence.',
    'long_description': '# ghost\nmanage your digital presence\n\n**Install**: `wget gh.ost.lol/ghost.py -q && python3 ghost.py`\n\n**Hosts:** [Digital Ocean](https://cloud.digitalocean.com/account/api/tokens)  \n**Registrars:** [Dynadot](https://www.dynadot.com/account/domain/setting/api.html)\n\n    $ wget gh.ost.lol/ghost.py -q && python3 ghost.py\n\n      _|_|_|  _|                              _|\n    _|        _|_|_|      _|_|      _|_|_|  _|_|_|_|\n    _|  _|_|  _|    _|  _|    _|  _|_|        _|\n    _|    _|  _|    _|  _|    _|      _|_|    _|\n      _|_|_|  _|    _|    _|_|    _|_|_|        _|_|\n\n    spawning a new presence..\n    presence name: testing\n    digital ocean token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n    generating droplet..\n    machine initialized at: xxx.xx.xx.xxx\n\n    spawning sudoer `ghost`..\n\n    setting up base system..\n      0:00 updating\n      0:09 upgrading\n      0:55 installing system packages\n      3:24 installing Python 3.9.2\n      3:24   downloading\n      3:25   extracting\n      3:28   configuring\n      4:07   making\n      8:54   installing\n      9:50 creating virtual environment\n      9:59 installing SQLite\n      9:59   downloading\n     10:00   extracting\n     10:01   configuring\n     12:25 installing Ghost\n     13:29 installing Nginx 1.18.0\n     13:29   downloading\n     13:31   extracting\n     13:31   configuring\n     13:42   making\n     14:55   installing\n     14:55 generating a large prime for TLS\n\n     You may now sign in to your host while installation continues:\n         https://165.227.30.1?secret=sepkpt\n\n     14:59 installing Tor 0.4.4.5\n     14:59   downloading\n     15:01   extracting\n     15:02   configuring\n     15:34   making\n     24:47   installing\n     24:50 installing Firefox-82.0\n     25:14 installing Geckodriver-0.27.0\n\n![](https://github.com/angelogladding/ghost/raw/main/interface.png)\n',
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
