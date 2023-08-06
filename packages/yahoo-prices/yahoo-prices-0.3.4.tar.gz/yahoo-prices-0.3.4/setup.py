# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yahoo_prices']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.23,<2.0.0',
 'pandas-datareader>=0.9.0,<0.10.0',
 'pandas>=1.2.3,<2.0.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'yahoo-prices',
    'version': '0.3.4',
    'description': '',
    'long_description': None,
    'author': 'aghazaly',
    'author_email': 'ghazaly_7000@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
