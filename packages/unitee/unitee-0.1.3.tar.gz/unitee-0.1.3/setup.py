# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unitee']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unitee',
    'version': '0.1.3',
    'description': 'super simple units',
    'long_description': None,
    'author': '0Hughman0',
    'author_email': 'rammers2@hotmail.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
