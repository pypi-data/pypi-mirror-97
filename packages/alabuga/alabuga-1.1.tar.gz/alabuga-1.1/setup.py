# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alabuga', 'alabuga.migrations']

package_data = \
{'': ['*'], 'alabuga': ['static/alabuga/js/*', 'templates/alabuga/*']}

setup_kwargs = {
    'name': 'alabuga',
    'version': '1.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
