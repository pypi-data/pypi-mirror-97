# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['outcome', 'outcome.peewee_validates']

package_data = \
{'': ['*']}

install_requires = \
['peewee>=3.13.3,<4.0.0', 'python-dateutil>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'outcome-peewee-validates',
    'version': '2.0.0',
    'description': 'Fork of Peewee-validates',
    'long_description': '# peewee-validates-py\n![Continuous Integration](https://github.com/outcome-co/peewee-validates-py/actions/workflows/ci.py.opensource.yaml/badge.svg) ![version-badge](https://img.shields.io/badge/version-2.0.0-brightgreen)\n\nValidation library for peewee.\n\n## Usage\n\n```sh\npoetry add outcome-peewee-validates\n```\n\n## Development\n\nRemember to run `./bootstrap.sh` when you clone the repository.\n',
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/peewee-validates-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
