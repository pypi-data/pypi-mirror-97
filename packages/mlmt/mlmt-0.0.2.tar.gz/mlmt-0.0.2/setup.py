# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlmt']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mlmt',
    'version': '0.0.2',
    'description': 'A Machine Learning Multi-Tool',
    'long_description': '# A Machine Learning Multi-Tool (mlmt)\n\nA collection of loosely organized code to assist machine learning research.\n\n## Installation\n\n```sh\npip install --upgrade mlmt\n```\n\n## Usage\n\n```python\nimport mlmt\n```\n',
    'author': 'Rick Lan',
    'author_email': 'rlan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlan/mlmt',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
