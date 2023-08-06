# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jokeapi']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.4,<4.0.0',
 'pytest>=6.2.1,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'simplejson>=3.17.2,<4.0.0',
 'urllib3>=1.26.2,<2.0.0']

setup_kwargs = {
    'name': 'jokeapi',
    'version': '0.2.10',
    'description': "An API wrapper for Sv443's JokeAPI",
    'long_description': None,
    'author': 'leet hakker',
    'author_email': 'leet_haker@cyber-wizard.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
