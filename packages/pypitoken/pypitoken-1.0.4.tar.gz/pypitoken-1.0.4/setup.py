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
    'version': '1.0.4',
    'description': 'Manipulate PyPI API tokens',
    'long_description': 'PyPIToken: Manipulate PyPI API tokens\n=====================================\n\n.. image:: https://img.shields.io/pypi/v/pypitoken?logo=pypi&logoColor=white\n    :target: https://pypi.org/pypi/pypitoken\n    :alt: Deployed to PyPI\n\n.. image:: https://img.shields.io/pypi/pyversions/pypitoken?logo=pypi&logoColor=white\n    :target: https://pypi.org/pypi/pypitoken\n    :alt: Deployed to PyPI\n\n.. image:: https://img.shields.io/github/stars/ewjoachim/pypitoken?logo=github\n    :target: https://github.com/ewjoachim/pypitoken/\n    :alt: GitHub Repository\n\n.. image:: https://img.shields.io/github/workflow/status/ewjoachim/pypitoken/CI?logo=github\n    :target: https://github.com/ewjoachim/pypitoken/actions?workflow=CI\n    :alt: Continuous Integration\n\n.. image:: https://img.shields.io/readthedocs/pypitoken?logo=read-the-docs&logoColor=white\n    :target: http://pypitoken.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation\n\n.. image:: https://img.shields.io/codecov/c/github/ewjoachim/pypitoken?logo=codecov&logoColor=white\n    :target: https://codecov.io/gh/ewjoachim/pypitoken\n    :alt: Coverage\n\n.. image:: https://img.shields.io/github/license/ewjoachim/pypitoken?logo=open-source-initiative&logoColor=white\n    :target: https://github.com/ewjoachim/pypitoken/blob/master/LICENSE\n    :alt: MIT License\n\n.. image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg\n    :target: https://github.com/ewjoachim/pypitoken/blob/master/CODE_OF_CONDUCT.md\n    :alt: Contributor Covenant\n\n\nPyPIToken is an open-source Python 3.6+ library for generating and manipulating\nPyPI tokens.\n\nPyPI tokens are very powerful, as that they are based on Macaroons_. They allow\nthe bearer to add additional restrictions to an existing token. For example, given\na PyPI token that can upload releases for any project of its owner, you can generate\na token that will only allow some projects, or even a single one.\n\n.. _macaroons: https://en.wikipedia.org/wiki/Macaroons_(computer_science)\n\nHere\'s an example:\n\n.. code-block:: console\n\n    $ pip install pypitoken\n\n.. code-block:: python\n\n    import pypitoken\n\n    token = pypitoken.Token.load("pypi-foobartoken")\n\n    print(token.restrictions)\n    # [NoopRestriction()]\n\n    token.restrict(projects=["requests"])\n\n    print(token.restrictions)\n    # [NoopRestriction(), ProjectsRestriction(projects=["requests"])]\n\n    token.dump()\n    # pypi-newfoobartoken\n\nThis token we\'ve created above will be restricted to uploading releases of ``requests``.\nOf course, your PyPI user will still need to have upload permissions on ``requests``\nfor this to happen.\n\nThe aim of this library is to provide a simple toolbelt for manipulating PyPI tokens.\nIdeally, someday, PyPI (Warehouse_) itself may generate their tokens using this\nlibrary too. This should make it easier to iterate on new kinds of restrictions for\nPyPI tokens, such as those discussed in the `original implementation issue`__:\n\n- Tokens scoped to a specific time interval\n- Tokens scoped to uploading a given version\n- Tokens scopes to uploading a given release\n- Tokens scopes to uploading a file with a given hash\n- (Maybe even one-time tokens)\n\n.. _Warehouse: https://github.com/pypa/warehouse/\n.. __: https://github.com/pypa/warehouse/issues/994\n\n.. Below this line is content specific to the README that will not appear in the doc.\n.. end-of-index-doc\n\nWhere to go from here\n---------------------\n\nThe complete docs_ is probably the best place to learn about the project.\n\nIf you encounter a bug, or want to get in touch, you\'re always welcome to open a\nticket_.\n\n.. _docs: http://pypitoken.readthedocs.io/en/latest\n.. _ticket: https://github.com/ewjoachim/pypitoken/issues/new\n',
    'author': 'Joachim Jablon',
    'author_email': 'ewjoachim@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypitoken.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
