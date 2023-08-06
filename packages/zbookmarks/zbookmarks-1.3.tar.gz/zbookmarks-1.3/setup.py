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
    'version': '1.3',
    'description': 'Load / dump Chrome bookmark files',
    'long_description': '### Install\n\n```console\n$ pip install zbookmarks\n```\n\n### Usage\n\nA simple python package for loading / dumping Chrome HTML bookmarks.\nBorn out of necessity to fix my own bookmarks.\n\n```python\nimport zbookmarks\n\n# Load\nwith open("chrome_bookmarks.html", "r") as f:\n    bookmarks = zbookmarks.load_chrome(f.read())\n\n# Print\nprint(bookmarks)\n\n# Dump\nwith open("output.html", "w") as f:\n    zbookmarks.dump_chrome(bookmarks, f)\n```\n\n\n### How it works\n\nI made this package by examining my own Chrome bookmark files and extrapolating.\nThe general rules are:\n- `dl` denotes a list of bookmark items and folders.\n- `dt` denotes either a bookmark item or folder:\n    - If it\'s a bookmark item, `dt` has a single `a` tag child, which gives the\n      bookmark attributes (href, title, etc.).\n    - If it\'s a bookmark folder, `dt` has 3 children:\n        - A `h3` tag containing the folder attributes (title, etc.)\n        - A `dl` tag containing the folder\'s contents.\n        - A useless `p` child tag.\n\nI found it easier to come up with these rules after visualizing the DOM tree of\na Chrome bookmarks file:\n\n![Visualize DOM tree of bookmarks file](scripts/dom.svg)\n\nYou can try it out on your own bookmark file by running:\n```console\n# You need to install graphviz (dot) in order to run the script\n$ sudo apt-get install -y graphviz\n$ poetry install\n$ python3 scripts/visualize_dom.py <my_bookmarks_file.html>\n```\n',
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
