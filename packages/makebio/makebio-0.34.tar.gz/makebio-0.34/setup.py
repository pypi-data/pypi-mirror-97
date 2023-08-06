# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makebio']

package_data = \
{'': ['*'], 'makebio': ['config/*']}

install_requires = \
['click>=7.0,<8.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['makebio = makebio.cli:cli']}

setup_kwargs = {
    'name': 'makebio',
    'version': '0.34',
    'description': 'Manage your computational biology research projects',
    'long_description': None,
    'author': 'Vivek Rai',
    'author_email': 'vivekrai@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
