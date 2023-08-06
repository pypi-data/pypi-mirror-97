# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hallo_ut']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'hallo-ut',
    'version': '0.1.0',
    'description': '',
    'long_description': '# hallo-ut\nLayanan Informasi Universitas Terbuka\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
