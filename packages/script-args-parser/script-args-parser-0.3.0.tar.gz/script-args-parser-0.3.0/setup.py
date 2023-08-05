# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['script_args_parser']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'script-args-parser',
    'version': '0.3.0',
    'description': 'Script arguments parsing library.',
    'long_description': None,
    'author': 'KRunchPL',
    'author_email': 'krunchfrompoland@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
