# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzohoapi',
 'pyzohoapi.core',
 'pyzohoapi.exceptions',
 'pyzohoapi.objecttypes',
 'pyzohoapi.objecttypes.mixins']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyzohoapi',
    'version': '0.4.1',
    'description': 'Pythonic access to Zoho APIs in the Finance Plus suite.',
    'long_description': '# pyZohoAPI (v0.4.1)\n **pyZohoAPI** provides Pythonic access to Zoho APIs in the Finance Plus suite:\n * **Books**\n * *Checkout*<sup>*</sup>\n * *Expense*<sup>*</sup>\n * **Inventory**\n * *Invoice*<sup>*</sup>\n * *Subscriptions*<sup>*</sup>\n\n<sup>*</sup> Support is planned, but not yet available.\n\n[![PyPI](https://img.shields.io/pypi/v/pyzohoapi)](https://pypi.org/project/pyzohoapi/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyzohoapi)](https://pypi.org/project/pyzohoapi/)\n![License](https://img.shields.io/github/license/tdesposito/pyZohoAPI)\n[![Documentation Status](https://readthedocs.org/projects/pyzohoapi/badge/?version=latest)](https://pyzohoapi.readthedocs.io/en/latest/?badge=latest)\n\n## Installing pyZohoAPI\n<!-- start installation -->\n\nYou\'ll need at least **Python 3.6** to install pyZohoAPI.\n\n### Via PyPI\n```console\n$ python -m pip install pyzohoapi\n```\n\n### From Source\nWe use [Poetry](https://python-poetry.org/) for virtual environment and\ndependency management.\n```console\n$ git clone https://github.com/tdesposito/pyZohoAPI.git\n$ cd pyZohoAPI\n$ poetry install\n$ poetry build\n$ pip install dist/*.whl\n```\n<!-- end installation -->\n\n## Basic Usage\n\n<!-- start basic-usage -->\n```python\n>>> from pyzohoapi import ZohoInventory\n>>> api = ZohoInventory("{your-orginization-id}", "{your-region}",\n...   client_id="{your-client-id}",\n...   client_secret="{your-client-secret}",\n...   refresh_token="{your-refresh-token}"\n... )\n>>> contact = api.Contact(email="test@example.com").First()\n>>> contact.IsLoaded\nTrue\n>>> contact.first_name\n\'test\'\n>>> contact.first_name = "Changed"\n>>> contact.Update()\n```\n<!-- end basic-usage -->\n\nSee the [full documetation on ReadTheDocs](https://pyzohoapi.readthedocs.io/en/latest/)\n\n## Contributing\nPull Requests gladly considered!\n',
    'author': 'Todd Esposito',
    'author_email': 'todd@toddesposito.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tdesposito/pyZohoAPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
