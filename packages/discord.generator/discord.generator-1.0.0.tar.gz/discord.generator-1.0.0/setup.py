# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['discord.generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'discord.generator',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Oleg',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
