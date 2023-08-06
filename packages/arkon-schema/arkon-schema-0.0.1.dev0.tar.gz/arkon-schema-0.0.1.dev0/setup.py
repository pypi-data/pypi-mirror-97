# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkon_schema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'arkon-schema',
    'version': '0.0.1.dev0',
    'description': 'Arkon protobuf library',
    'long_description': None,
    'author': 'Nick Groszewski',
    'author_email': 'groszewn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
