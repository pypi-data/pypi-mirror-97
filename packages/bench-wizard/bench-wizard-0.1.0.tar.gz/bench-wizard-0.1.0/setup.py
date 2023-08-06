# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bench_wizard']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['benchwizard = bench_wizard.main:main']}

setup_kwargs = {
    'name': 'bench-wizard',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Martin Hloska',
    'author_email': 'martin.hloska@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
