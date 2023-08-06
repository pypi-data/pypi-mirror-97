# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypitoken']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema', 'pymacaroons>=0.13.0,<0.14.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses']}

setup_kwargs = {
    'name': 'pypitoken',
    'version': '1.0.3',
    'description': 'Manipulate PyPI API tokens',
    'long_description': None,
    'author': 'Joachim Jablon',
    'author_email': 'ewjoachim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
