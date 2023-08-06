# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cwmungo']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=4.5.1,<5.0.0']

setup_kwargs = {
    'name': 'cwmungo',
    'version': '0.1.0',
    'description': 'Extract crossword grids from images',
    'long_description': None,
    'author': 'Harry Slatyer',
    'author_email': 'harry.slatyer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
