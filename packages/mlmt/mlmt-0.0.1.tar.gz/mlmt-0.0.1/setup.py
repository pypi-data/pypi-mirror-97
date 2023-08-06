# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlmt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mlmt',
    'version': '0.0.1',
    'description': 'A Machine Learning Multi-Tool',
    'long_description': None,
    'author': 'Rick Lan',
    'author_email': 'rlan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
