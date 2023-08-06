# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dbd_py']
setup_kwargs = {
    'name': 'dbd-py',
    'version': '0.2.0',
    'description': 'Cool Discord Bot Designer module for python by Edited Cocktail',
    'long_description': None,
    'author': 'Edited Cockatail',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
