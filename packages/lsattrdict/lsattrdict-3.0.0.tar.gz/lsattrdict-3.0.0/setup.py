# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lsattrdict']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lsattrdict',
    'version': '3.0.0',
    'description': 'fork of dead AttrDict project',
    'long_description': None,
    'author': 'Marco Bartel',
    'author_email': 'bsimpson888@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
