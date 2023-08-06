# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ttor_test_pypi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ttor-test-pypi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Travis Torline',
    'author_email': 'travis.torline@workiva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
