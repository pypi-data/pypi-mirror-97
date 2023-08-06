# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routeros_diff', 'routeros_diff.commands']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['ros_diff = routeros_diff.commands.diff:run',
                     'ros_prettify = routeros_diff.commands.prettify:run',
                     'routeros_diff = routeros_diff.commands.diff:run',
                     'routeros_prettify = routeros_diff.commands.prettify:run']}

setup_kwargs = {
    'name': 'routeros-diff',
    'version': '0.1.0',
    'description': 'Tools for parsing & diffing RouterOS configuration files. Can produce config file patches.',
    'long_description': None,
    'author': 'Adam Charnock',
    'author_email': 'adam.charnock@gardunha.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gardunha/routeros-diff',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
