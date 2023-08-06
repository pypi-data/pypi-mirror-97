# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['groepszoeker']
setup_kwargs = {
    'name': 'groepszoeker',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Graham Binns',
    'author_email': 'graham@outcoded.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
