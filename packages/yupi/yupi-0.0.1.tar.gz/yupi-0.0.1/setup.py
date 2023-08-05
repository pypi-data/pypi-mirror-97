# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yupi', 'yupi.tracking']

package_data = \
{'': ['*'], 'yupi': ['cameras/*']}

install_requires = \
['PyQt5>=5.15.3,<6.0.0',
 'matplotlib>=3.2.0',
 'nudged>=0.3.1',
 'numpy>=1.16.5',
 'opencv-python>=4.4.0']

setup_kwargs = {
    'name': 'yupi',
    'version': '0.0.1',
    'description': 'A package for tracking and analysing objects trajectories',
    'long_description': '# Yupi\n\nLong description of the package\n',
    'author': 'Gustavo Viera-López',
    'author_email': 'gvieralopez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
