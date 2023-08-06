# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idp_solver']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0',
 'pretty-errors>=1.2.19,<2.0.0',
 'sphinxcontrib-mermaid==0.6.3',
 'textX>=2.1.0,<3.0.0',
 'z3-solver==4.8.8.0']

entry_points = \
{'console_scripts': ['idp-solver = idp_solver.IDP_Z3:cli']}

setup_kwargs = {
    'name': 'idp-solver',
    'version': '0.7.3',
    'description': 'IDP-Z3 is a collection of software components implementing the Knowledge Base paradigm using the IDP language and a Z3 SMT solver.',
    'long_description': 'This package is deprecated.\n\nPlease use [idp-engine](https://pypi.org/project/idp-engine/) instead.',
    'author': 'pierre.carbonnelle',
    'author_email': 'pierre.carbonnelle@cs.kuleuven.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.idp-z3.be',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
