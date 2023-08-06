# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archmd']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['archmd = archmd:app']}

setup_kwargs = {
    'name': 'archmd',
    'version': '0.1.0',
    'description': 'A simple command line utility to build an architecture.md file',
    'long_description': None,
    'author': 'Joel Collins',
    'author_email': 'pypi@jtcollins.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
