# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hallo_ut']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'bleach>=3.3.0,<4.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['hallo-ut = hallo_ut.__main__:main']}

setup_kwargs = {
    'name': 'hallo-ut',
    'version': '0.3.0',
    'description': 'SDK Python Layanan Informasi & Bantuan Universitas Terbuka',
    'long_description': '# hallo-ut\n\n[![hallo-ut - PyPi](https://img.shields.io/pypi/v/hallo-ut)](https://pypi.org/project/hallo-ut/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/hallo-ut)](https://pypi.org/project/hallo-ut/)\n[![LICENSE](https://img.shields.io/github/license/UnivTerbuka/hallo-ut)](https://github.com/UnivTerbuka/hallo-ut/blob/main/LICENSE)\n[![Code Style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nSDK Python Layanan Informasi & Bantuan Universitas Terbuka\n\n## Install\n\nInstall dengan [python](https://www.python.org/)\n\n```bash\npip install --upgrade hallo-ut\n```\n\n## Penggunaan\n\nPenggunaan sederhana\n\n```bash\npython -m hallo-ut "pertanyaan anda atau tiket hallo-ut anda"\n```\n',
    'author': 'hexatester',
    'author_email': 'habibrohman@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
