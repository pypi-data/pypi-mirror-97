# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyask']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyask',
    'version': '0.1.7',
    'description': 'Library for terminal programs to ask users questions.',
    'long_description': '# `pyask`\n\nA library for terminal programs to ask users questions.\n',
    'author': 'Thomas M Ward',
    'author_email': 'thomas@thomasward.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tmward/pypask',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
