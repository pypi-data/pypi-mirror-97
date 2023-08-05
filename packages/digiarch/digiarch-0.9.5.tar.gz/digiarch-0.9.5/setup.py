# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['digiarch', 'digiarch.core', 'digiarch.database', 'digiarch.models']

package_data = \
{'': ['*'], 'digiarch': ['_data/*']}

install_requires = \
['acamodels>=0.5.3,<0.6.0',
 'click>=7.0,<8.0',
 'dacite>=1.0,<2.0',
 'databases[sqlite]>=0.3.2,<0.5.0',
 'natsort>=7.0.1,<8.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sqlalchemy>=1.3.19,<2.0.0',
 'sqlalchemy_utils>=0.36.8,<0.37.0',
 'tqdm>=4.36,<5.0']

entry_points = \
{'console_scripts': ['digiarch = digiarch.cli:cli']}

setup_kwargs = {
    'name': 'digiarch',
    'version': '0.9.5',
    'description': 'Tools for the Digital Archive Project at Aarhus Stadsarkiv',
    'long_description': '[![Aarhus Stadsarkiv](https://raw.githubusercontent.com/aarhusstadsarkiv/py-template/master/img/logo.png)](https://stadsarkiv.aarhus.dk/)\n# Digital Archive [![Tests](https://github.com/aarhusstadsarkiv/digiarch/workflows/Tests/badge.svg?branch=master)](https://github.com/aarhusstadsarkiv/digiarch/actions?query=workflow%3ATests+branch%3Amaster) [![codecov](https://codecov.io/gh/aarhusstadsarkiv/digiarch/branch/master/graph/badge.svg)](https://codecov.io/gh/aarhusstadsarkiv/digiarch) [![PyPI](https://badge.fury.io/py/digiarch.svg)](https://badge.fury.io/py/digiarch)\nThis repository contains code pertaining to the Digital Archive Project at Aarhus Stadsarkiv.\n',
    'author': 'Nina Jensen',
    'author_email': 'jnik@aarhus.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://stadsarkiv.aarhus.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
