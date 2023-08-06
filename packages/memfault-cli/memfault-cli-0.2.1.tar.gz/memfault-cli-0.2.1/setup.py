# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memfault_cli']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0',
 'more_itertools>=8.0.2,<9.0.0',
 'pyelftools>=0.26.0,<0.27.0',
 'requests>=2.22.0,<3.0.0',
 'tqdm>=4.44.1,<5.0.0']

entry_points = \
{'console_scripts': ['memfault = memfault_cli.cli:main']}

setup_kwargs = {
    'name': 'memfault-cli',
    'version': '0.2.1',
    'description': 'Memfault CLI tool',
    'long_description': '# Memfault CLI tool\n\nThis package contains the `memfault` CLI tool.\n\nThe purpose of the tool is to make integration with Memfault from other systems,\nlike continuous integration servers, as easy as possible.\n\nInstall the tool and run `memfault --help` for more info!\n',
    'author': 'Memfault Inc',
    'author_email': 'hello@memfault.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.memfault.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
