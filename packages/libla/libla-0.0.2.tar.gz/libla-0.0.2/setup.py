# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libla']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'scipy>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'libla',
    'version': '0.0.2',
    'description': 'A Linear Algebra Library for Python/numpy',
    'long_description': None,
    'author': 'Heinrich Hartmann',
    'author_email': 'heinrich@heinrichhartmann.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
