# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_store_cli']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tg-store-cli = tg_store_cli.main:main']}

setup_kwargs = {
    'name': 'tg-store-cli',
    'version': '0.4.0',
    'description': '',
    'long_description': '# `tg-store-cli`\n\nTG Store CLI\n\n**Usage**:\n\n```console\n$ tg-store-cli [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `load`: Зарядка\n* `shoot`: Стрельба\n\n## `tg-store-cli load`\n\nЗарядка\n\n**Usage**:\n\n```console\n$ tg-store-cli load [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `tg-store-cli shoot`\n\nСтрельба \n\n**Usage**:\n\n```console\n$ tg-store-cli shoot [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
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
