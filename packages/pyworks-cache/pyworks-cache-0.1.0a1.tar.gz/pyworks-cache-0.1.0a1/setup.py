# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyworks_cache']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'pyworks-cache',
    'version': '0.1.0a1',
    'description': 'Provide quick and simple function for caching use Redis or Files.',
    'long_description': '# pyworks-cache\nPyworks Cache provide quick and simple function for caching use Redis or Files.\n',
    'author': 'PyWorks Asia Team',
    'author_email': 'opensource@pyworks.asia',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyworksasia/pyworks-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
