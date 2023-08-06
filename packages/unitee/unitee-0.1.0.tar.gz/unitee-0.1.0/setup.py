# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['unitee']
setup_kwargs = {
    'name': 'unitee',
    'version': '0.1.0',
    'description': 'super simple units',
    'long_description': None,
    'author': '0Hughman0',
    'author_email': 'rammers2@hotmail.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
