# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipda']

package_data = \
{'': ['*']}

install_requires = \
['executing', 'varname']

setup_kwargs = {
    'name': 'pipda',
    'version': '0.1.4',
    'description': 'A framework for data piping in python',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
