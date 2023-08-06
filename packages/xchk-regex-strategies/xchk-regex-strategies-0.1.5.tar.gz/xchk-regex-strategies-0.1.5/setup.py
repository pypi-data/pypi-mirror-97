# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xchk_regex_strategies']

package_data = \
{'': ['*']}

install_requires = \
['regex>=2020.7.14,<2021.0.0']

setup_kwargs = {
    'name': 'xchk-regex-strategies',
    'version': '0.1.5',
    'description': 'Checking strategies for xchk based around regular expressions.',
    'long_description': None,
    'author': 'Vincent Nys',
    'author_email': 'vincentnys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
