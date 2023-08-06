# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zbookmarks']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'zbookmarks',
    'version': '1.2',
    'description': 'Load / dump Chrome bookmark files',
    'long_description': None,
    'author': 'Yannis Zarkadas',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
