# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiosteady']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'attrs>=20.3.0,<21.0.0']

setup_kwargs = {
    'name': 'aiosteady',
    'version': '0.1.0',
    'description': 'Rate limiting for asyncio',
    'long_description': 'aiosteady: rate limiting for asyncio\n====================================\n\n.. image:: https://img.shields.io/pypi/v/aiosteady.svg\n        :target: https://pypi.python.org/pypi/aiosteady\n\n.. image:: https://travis-ci.org/Tinche/aiosteady.svg?branch=master\n        :target: https://travis-ci.org/Tinche/aiosteady\n\n.. image:: https://codecov.io/gh/Tinche/aiosteady/branch/master/graph/badge.svg\n        :target: https://codecov.io/gh/Tinche/aiosteady\n\n.. image:: https://img.shields.io/pypi/pyversions/aiosteady.svg\n        :target: https://github.com/Tinche/aiosteady\n        :alt: Supported Python versions\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n**aiosteady** is an Apache2 licensed library, written in Python, for rate limiting\nin asyncio application using Redis.',
    'author': 'Tin Tvrtkovic',
    'author_email': 'tinchester@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
