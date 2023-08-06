# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Robin Allesiardo',
    'author_email': 'robin.allesiardo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rallesiardo/random_tools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
