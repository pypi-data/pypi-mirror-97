# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_agar_core', 'datek_agar_core.network']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'datek-app-utils>=0.2.0,<0.3.0',
 'msgpack>=1.0.2,<2.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pydantic>=1.7.3,<2.0.0']

extras_require = \
{'uvloop': ['uvloop>=0.14.0,<0.15.0']}

entry_points = \
{'console_scripts': ['run-server = datek_agar_core.run_server:run_server']}

setup_kwargs = {
    'name': 'datek-agar-core',
    'version': '0.1.0',
    'description': 'Agar game core',
    'long_description': "[![pipeline status](https://gitlab.com/datek-agar/agar-core/badges/master/pipeline.svg)](https://gitlab.com/datek-agar/agar-core/-/commits/master)\n[![coverage report](https://gitlab.com/datek-agar/agar-core/badges/master/coverage.svg)](https://gitlab.com/datek-agar/agar-core/-/commits/master)\n\n# Agar game core\n\nThe project contains the game logic, the rules of this universe, the server and an async client.\nIt's in early stage of development.\n\n\n## Installation\nIf your OS is compatible with `uvloop`, install it with `pip install datek-agar-core[uvloop]`\n\n\n## Usage\nAfter installing, just type `run-server` in the terminal.\nFor help, type `run-server --help`\n",
    'author': 'DAtek',
    'author_email': 'dudasa7@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/datek-agar/agar-core',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
