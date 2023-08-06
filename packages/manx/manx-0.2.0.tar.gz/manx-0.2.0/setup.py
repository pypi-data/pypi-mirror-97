# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manx']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch[async]>=7.10.1,<8.0.0']

setup_kwargs = {
    'name': 'manx',
    'version': '0.2.0',
    'description': 'Data migrations for elasticsearch',
    'long_description': None,
    'author': 'Eric Grunzke',
    'author_email': 'Eric.Grunzke@concentrix.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
