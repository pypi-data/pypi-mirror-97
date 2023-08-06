# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yupi', 'yupi.analyzing', 'yupi.tracking']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.3,<6.0.0',
 'matplotlib>=3.2.0',
 'nudged>=0.3.1',
 'numpy>=1.16.5',
 'opencv-python>=4.4.0']

setup_kwargs = {
    'name': 'yupi',
    'version': '0.2.0',
    'description': 'A package for tracking and analysing objects trajectories',
    'long_description': '# yupi\n\nStanding for *Yet Underused Path Instruments*, yupi is a set of tools designed for collecting and processing trajectory data. A detailed description of the API can be found in the [official documentation](https://yupi.readthedocs.io/en/latest/). Code examples (with additional multimedia resources) can be found in [this repository](https://github.com/yupidevs/yupi_examples).\n\n## Instalation\n\nCurrent recommended installation method is via the pypi package:\n\n```cmd\npip install yupi\n```\n',
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
