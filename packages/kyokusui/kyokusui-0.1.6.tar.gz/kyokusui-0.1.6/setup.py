# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kyokusui']

package_data = \
{'': ['*'],
 'kyokusui': ['static/*',
              'static/highlight/*',
              'templates/*',
              'templates/components/*']}

setup_kwargs = {
    'name': 'kyokusui',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'boke0',
    'author_email': 'speken00.tt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
