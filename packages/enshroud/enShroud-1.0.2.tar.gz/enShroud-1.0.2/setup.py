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
    'version': '1.0.2',
    'description': 'A steganography tool to hide secret texts in white space.',
    'long_description': '# enShroud\n\n![](/img/enShroud.png)\n\n## Introduction\n\nA steganography tool to hide secret texts in white space.\n\n## Usage:\n\n- To encode:\n\n```python\npython3 enShroud.py -e -p PATH_TO_TEXT_FILE -o PATH_TO_OUTPUT -s "SECRET_MESSAGE_IN_QUOTES"\n```\n\n- To decode:\n\n```python\npython3 enShroud.py -d -p PATH_TO_TEXT_FILE\n```\n',
    'author': 'Akarsh Malik',
    'author_email': 'malikakarsh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/malikakarsh/enShroud.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
