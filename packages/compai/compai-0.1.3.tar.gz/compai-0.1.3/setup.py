# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compai']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['importlib-metadata>=3.7.0,<4.0.0'],
 'docs': ['mkdocs>=1.1.2,<2.0.0',
          'mkdocstrings>=0.15.0,<0.16.0',
          'mkdocs-material>=7.0.4,<8.0.0']}

setup_kwargs = {
    'name': 'compai',
    'version': '0.1.3',
    'description': 'Functional primitives for python',
    'long_description': '# Compai\n\n> Functional primitives for python\n\n[![Python package](https://github.com/frndmg/compai/actions/workflows/python-package.yml/badge.svg?branch=master)](https://github.com/frndmg/compai/actions/workflows/python-package.yml)\n[![PyPI Package latest release](https://img.shields.io/pypi/v/compai.svg)](https://pypi.org/project/compai/)\n[![codecov](https://codecov.io/gh/frndmg/compai/branch/master/graph/badge.svg?token=CYKFXTI0Z7)](https://codecov.io/gh/frndmg/compai)\n',
    'author': 'Fernando Martínez González',
    'author_email': 'frndmartinezglez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frndmg/compai',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
