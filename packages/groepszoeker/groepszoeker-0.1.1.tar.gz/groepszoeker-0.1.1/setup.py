# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['groepszoeker']
setup_kwargs = {
    'name': 'groepszoeker',
    'version': '0.1.1',
    'description': 'A library for finding sub-populations within a group of numerical values.',
    'long_description': None,
    'author': 'Graham Binns',
    'author_email': 'graham@outcoded.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/gmb/groepszoeker',
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
