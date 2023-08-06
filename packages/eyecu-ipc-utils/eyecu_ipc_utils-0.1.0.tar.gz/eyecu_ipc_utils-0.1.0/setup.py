# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['OnvifClient']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eyecu-ipc-utils',
    'version': '0.1.0',
    'description': 'Modern IP Camera Clients, ONVIF',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
