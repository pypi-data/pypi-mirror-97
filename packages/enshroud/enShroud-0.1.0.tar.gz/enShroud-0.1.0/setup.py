# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enshroud']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['enShroud = enshroud.enshroud:main']}

setup_kwargs = {
    'name': 'enshroud',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Akarsh Malik',
    'author_email': 'malikakarsh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
