# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['search_that_hash',
 'search_that_hash.cracker',
 'search_that_hash.cracker.fast_mode_mod',
 'search_that_hash.cracker.greppable_mode_mod',
 'search_that_hash.cracker.offline_mod',
 'search_that_hash.cracker.online_mod',
 'search_that_hash.cracker.sth_mod']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'cloudscraper>=1.2.56,<2.0.0',
 'coloredlogs>=15.0,<16.0',
 'loguru>=0.5.3,<0.6.0',
 'name-that-hash>=1.1.6,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.12.2,<10.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['search-that-hash = search_that_hash.__main__:main',
                     'sth = search_that_hash.__main__:main']}

setup_kwargs = {
    'name': 'search-that-hash',
    'version': '0.2.3',
    'description': 'Search hashes quickly before cracking them',
    'long_description': None,
    'author': 'brandon',
    'author_email': 'brandon@skerritt.blog',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
