# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['projected_earnings']

package_data = \
{'': ['*']}

install_requires = \
['gspread>=3.7.0,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pandas>=1.2.3,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'projected-earnings',
    'version': '0.1.0',
    'description': 'Automate emails',
    'long_description': None,
    'author': 'DChambers95',
    'author_email': 'dichambers95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
