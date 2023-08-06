# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orinoco']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'orinoco',
    'version': '1.0.1',
    'description': 'Functional composable pipelines allowing clean separation of the business logic and its implementation',
    'long_description': None,
    'author': 'Martin Vo',
    'author_email': 'mvo@paysure.solutions',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
