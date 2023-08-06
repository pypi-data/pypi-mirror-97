# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libd',
    'version': '0.1.0',
    'description': 'This is a library that contains all the advanced data structures that are otherwise not supported by Python native library.',
    'long_description': None,
    'author': 'Tinu Tomson',
    'author_email': 'tinutomson@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
