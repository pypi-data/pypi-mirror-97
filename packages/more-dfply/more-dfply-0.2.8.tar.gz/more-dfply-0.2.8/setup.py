# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['more_dfply']

package_data = \
{'': ['*']}

install_requires = \
['composable>=0.2.5,<0.3.0', 'dfply>=0.3.3,<0.4.0']

setup_kwargs = {
    'name': 'more-dfply',
    'version': '0.2.8',
    'description': 'Helper functions for the dfply package',
    'long_description': None,
    'author': 'Todd Iverson',
    'author_email': 'tiverson@winona.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
