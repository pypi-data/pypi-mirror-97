# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypitoken']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'pymacaroons>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'pypitoken',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Joachim Jablon',
    'author_email': 'ewjoachim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
