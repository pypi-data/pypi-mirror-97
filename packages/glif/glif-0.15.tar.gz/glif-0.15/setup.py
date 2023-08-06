# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['glif']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'imageio>=2.9.0,<3.0.0']

entry_points = \
{'console_scripts': ['glif = glif.__main__:main']}

setup_kwargs = {
    'name': 'glif',
    'version': '0.15',
    'description': 'CLI tool for creating gifs from a glob pattern',
    'long_description': None,
    'author': 'Andy Jackson',
    'author_email': 'amjack100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
