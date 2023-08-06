# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kickredis', 'kickredis.granite']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.35.0,<2.0.0',
 'lightbus>=1.0.1,<2.0.0',
 'protobuf>=3.14.0,<4.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'python-configuration>=0.8.1,<0.9.0',
 'redis-astra>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'kickredis',
    'version': '0.3.0',
    'description': 'Kicker client library for redis',
    'long_description': None,
    'author': 'Alexi Polenur',
    'author_email': 'alexi@polenur.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
