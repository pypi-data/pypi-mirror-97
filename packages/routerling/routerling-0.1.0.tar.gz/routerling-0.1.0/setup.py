# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routerling']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'routerling',
    'version': '0.1.0',
    'description': 'Extremely Stupid Simmple, Blazing Fast, Get Out of your way immediately Microframework for building Python Web Applications.',
    'long_description': None,
    'author': 'Raymond Ortserga',
    'author_email': 'codesage@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
