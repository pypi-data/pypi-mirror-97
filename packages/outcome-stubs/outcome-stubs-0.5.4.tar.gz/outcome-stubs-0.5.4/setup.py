# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pactman-stubs', 'requests-stubs', 'starlette-stubs']

package_data = \
{'': ['*'], 'pactman-stubs': ['mock/*', 'verifier/*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'pactman>=2.28.0,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'outcome-stubs',
    'version': '0.5.4',
    'description': 'Stub files for various python packages.',
    'long_description': '# stubs-py\n![Continuous Integration](https://github.com/outcome-co/stubs-py/workflows/Continuous%20Integration/badge.svg) ![version-badge](https://img.shields.io/badge/version-0.5.4-brightgreen)\n\nStubs for various python packages.\n\nThey are often partial, sometimes incomplete.\n\n## Usage\n\n```sh\npoetry add outcome-stubs\n```\n\n## Development\n\nRemember to run `./bootstrap.sh` when you clone the repository.\n',
    'author': 'Outcome Engineering',
    'author_email': 'engineering@outcome.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcome-co/stubs-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
