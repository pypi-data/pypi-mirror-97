# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['RPA', 'RPA.core', 'RPA.core.locators']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0', 'webdrivermanager>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'rpaframework-core',
    'version': '6.1.0',
    'description': 'Core utilities used by RPA Framework',
    'long_description': 'rpaframework-core\n=================\n\nThis package is a set of core functionality and utilities used\nby `RPA Framework`_. It is not intended to be installed directly, but\nas a dependency to other projects.\n\n.. _RPA Framework: https://rpaframework.org\n',
    'author': 'RPA Framework',
    'author_email': 'rpafw@robocorp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rpaframework.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
