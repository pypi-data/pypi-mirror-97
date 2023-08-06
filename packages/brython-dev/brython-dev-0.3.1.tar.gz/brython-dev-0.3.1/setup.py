# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brython_dev', 'brython_dev.data']

package_data = \
{'': ['*'], 'brython_dev': ['templates/*']}

install_requires = \
['brython>=3.9.1,<4.0.0',
 'flask-threaded-sockets>=0.3.2,<0.4.0',
 'flask>=1.1.2,<2.0.0',
 'pyyaml>=5.4.1,<6.0.0',
 'websocket-client>=0.56.0,<0.57.0']

setup_kwargs = {
    'name': 'brython-dev',
    'version': '0.3.1',
    'description': 'Brython developer tools',
    'long_description': None,
    'author': 'Lorenzo Garcia',
    'author_email': 'lorenzogarciacalzadilla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
