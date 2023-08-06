# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome',
 'outcome.devkit',
 'outcome.devkit.invoke',
 'outcome.devkit.invoke.tasks']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'colored-traceback>=0.3.0,<0.4.0',
 'coverage>=5.0.3,<6.0.0',
 'flake8-breakpoint>=1.1.0,<2.0.0',
 'flake8-builtins>=1.5.2,<2.0.0',
 'flake8-colors>=0.1.6,<0.2.0',
 'flake8-commas>=2.0.0,<3.0.0',
 'flake8-if-expr>=1.0.0,<2.0.0',
 'flake8-mutable>=1.2.0,<2.0.0',
 'flake8-print>=3.1.4,<5.0.0',
 'flake8-pytest>=1.3,<2.0',
 'flake8-return>=1.1.1,<2.0.0',
 'flake8>=3.7.9,<4.0.0',
 'ipython>=7.13.0,<8.0.0',
 'isort>=4.3.21,<5.0.0',
 'magicinvoke>=2.4.5,<3.0.0',
 'outcome-read-toml>=2.1.1,<3.0.0',
 'outcome-stubs>=0.5.4,<0.6.0',
 'outcome-utils>=5.0.3,<6.0.0',
 'pactman>=2.28.0,<3.0.0',
 'pdbpp>=0.10.2,<0.11.0',
 'poetry==1.1.4',
 'pre-commit>=2.10.1,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pytest-asyncio>=0.12,<0.15',
 'pytest>=6.2.2,<7.0.0',
 'rich>=9.11.0,<10.0.0',
 'syrupy>=1.1.0,<2.0.0',
 'wemake-python-styleguide>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'outcome-devkit',
    'version': '6.3.0',
    'description': 'A package containing common dev dependencies for python projects.',
    'long_description': '# devkit-py\n![Continuous Integration](https://github.com/outcome-co/devkit-py/workflows/Continuous%20Integration/badge.svg) ![version-badge](https://img.shields.io/badge/version-6.3.0-brightgreen)\n\nA package containing common dev dependencies for python projects.\n\n## Usage\n\n```sh\npoetry add -D outcome-devkit\n```\n\n## Development\n\nRun `./bootstrap.sh` when you clone the repository to get set up.\n',
    'author': 'Douglas Willcocks',
    'author_email': 'douglas@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/devkit-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
