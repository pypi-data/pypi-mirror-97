# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nullpom']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nullpom',
    'version': '0.0.1',
    'description': 'test',
    'long_description': None,
    'author': 'tenajima',
    'author_email': 'tenajima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
