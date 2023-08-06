# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rnm']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'clean-text[gpl]>=0.3.0,<0.4.0',
 'loguru>=0.5.3,<0.6.0',
 'pandas>=1.1.5,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'rnm',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'KhalidCK',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
