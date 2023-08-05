# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devops_cli']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.19,<2.0.0', 'kubernetes>=12.0.1,<13.0.0', 'pika>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['devops-cli = devops_cli.main:main']}

setup_kwargs = {
    'name': 'devops-cli',
    'version': '0.1.0',
    'description': 'A CLI tool that provides useful functions to operate on the Vital Beats cluster.',
    'long_description': None,
    'author': 'Stephen Badger',
    'author_email': 'stephen.badger@vitalbeats.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
