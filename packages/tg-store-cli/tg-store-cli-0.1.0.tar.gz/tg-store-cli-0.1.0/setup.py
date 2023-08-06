# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_store_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tg-store-cli = tg_store_cli.main:app']}

setup_kwargs = {
    'name': 'tg-store-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Tg Store Cli\nКонсольная утилита для стора',
    'author': 'sellercoder',
    'author_email': 'veniamin4e@gmail.com',
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
