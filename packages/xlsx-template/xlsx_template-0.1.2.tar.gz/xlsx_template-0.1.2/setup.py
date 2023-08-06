# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlsx_template', 'xlsx_template.runtime']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.5.2,<2.0.0',
 'openpyxl>=3.0.5,<4.0.0',
 'pyparsing>=2.4.7,<3.0.0']

setup_kwargs = {
    'name': 'xlsx-template',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Sergei Sinitsyn',
    'author_email': 'sinitsinsv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
