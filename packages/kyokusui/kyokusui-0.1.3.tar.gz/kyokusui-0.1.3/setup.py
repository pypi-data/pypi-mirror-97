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

install_requires = \
['mitama>=4.5.8,<5.0.0']

setup_kwargs = {
    'name': 'kyokusui',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'boke0',
    'author_email': 'speken00.tt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
