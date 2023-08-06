# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terra_sdk',
 'terra_sdk.client',
 'terra_sdk.client.lcd',
 'terra_sdk.client.lcd.api',
 'terra_sdk.core',
 'terra_sdk.core.auth',
 'terra_sdk.core.auth.data',
 'terra_sdk.core.bank',
 'terra_sdk.core.distribution',
 'terra_sdk.core.gov',
 'terra_sdk.core.market',
 'terra_sdk.core.msgauth',
 'terra_sdk.core.oracle',
 'terra_sdk.core.params',
 'terra_sdk.core.slashing',
 'terra_sdk.core.staking',
 'terra_sdk.core.staking.data',
 'terra_sdk.core.treasury',
 'terra_sdk.core.wasm',
 'terra_sdk.key',
 'terra_sdk.util']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'attrs>=20.3.0,<21.0.0',
 'bech32>=1.2.0,<2.0.0',
 'bip32utils>=0.3.post4,<0.4',
 'ecdsa>=0.16.1,<0.17.0',
 'mnemonic>=0.19,<0.20',
 'nest-asyncio>=1.5.1,<2.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'terra-sdk',
    'version': '0.12.0',
    'description': 'The Python SDK for Terra',
    'long_description': '![logo](./docs/img/logo.png)\n\n## Table of Contents <!-- omit in toc -->\n\n- [Installation](#installation)\n- [For Maintainers](#for-maintainers)\n  - [Testing](#testing)\n  - [Code Quality](#code-quality)\n  - [Releasing a new version](#releasing-a-new-version)\n- [License](#license)\n\n## Installation\n\nTerra SDK requires **Python v3.7+**.\n\n```sh\n$ pip install -U terra-sdk\n```\n\n## For Maintainers\n\n**NOTE:** This section is for developers and maintainers of the Terra SDK for Python.\n\nTerra SDK uses [Poetry](https://python-poetry.org/) to manage dependencies. To get set up with all the\n\n```sh\n$ pip install poetry\n$ poetry install\n```\n\n### Testing\n\nTerra SDK provides tests for data classes and functions. To run them:\n\n```\n$ make test\n```\n\n### Code Quality\n\nTerra SDK uses Black, isort, and mypy for checking code quality and maintaining style:\n\n```\n$ make qa && make format\n```\n\n### Releasing a new version\n\n**NOTE**: This section only concerns approved publishers on PyPI. An automated release\nprocess will be run upon merging into the `master` branch.\n\nTo publish a new version on PyPI, bump the version on `pyproject.toml` and run:\n\n```\n$ make release\n```\n\n## License\n\nTerra SDK is licensed under the MIT License. More details are available [here](./LICENSE).\n',
    'author': 'Terraform Labs, PTE.',
    'author_email': 'engineering@terra.money',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.terra.money/sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
