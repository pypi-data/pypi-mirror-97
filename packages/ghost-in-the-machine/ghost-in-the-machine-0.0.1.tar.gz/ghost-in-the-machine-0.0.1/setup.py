# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ghost']
install_requires = \
['understory>=0.0.1-alpha.0,<0.0.2']

entry_points = \
{'web.apps': ['ghost = ghost:app']}

setup_kwargs = {
    'name': 'ghost-in-the-machine',
    'version': '0.0.1',
    'description': 'Host web applications.',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
