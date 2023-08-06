# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authdog']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['authdog = authdog.__main__:cli']}

setup_kwargs = {
    'name': 'authdog',
    'version': '0.1.0',
    'description': 'Authdog command line interface',
    'long_description': None,
    'author': 'David Barrat',
    'author_email': 'david@barrat.io',
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
