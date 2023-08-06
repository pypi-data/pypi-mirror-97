# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grash']

package_data = \
{'': ['*']}

install_requires = \
['bashlex>=0.15,<0.16', 'python-magic>=0.4.20,<0.5.0']

entry_points = \
{'console_scripts': ['grash = console:main']}

setup_kwargs = {
    'name': 'grash',
    'version': '0.1.1',
    'description': 'A dependency analysis tool for bash scripts',
    'long_description': None,
    'author': 'Colin McAllister',
    'author_email': 'colinmca242@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
