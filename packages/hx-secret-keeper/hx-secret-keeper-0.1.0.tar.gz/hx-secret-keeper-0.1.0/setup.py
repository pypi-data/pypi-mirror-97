# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hx_secret_keeper']

package_data = \
{'': ['*']}

install_requires = \
['aws_secretsmanager_caching>=1.1.1,<2.0.0', 'boto3>=1.17.23,<2.0.0']

setup_kwargs = {
    'name': 'hx-secret-keeper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sujay S Kumar',
    'author_email': 'sujay@hypersonix.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
