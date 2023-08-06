# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compai']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['mkdocs>=1.1.2,<2.0.0',
          'mkdocstrings>=0.15.0,<0.16.0',
          'mkdocs-material>=7.0.4,<8.0.0']}

setup_kwargs = {
    'name': 'compai',
    'version': '0.1.2',
    'description': 'Cool functional primitives to have',
    'long_description': None,
    'author': 'Fernando Martínez González',
    'author_email': 'frndmartinezglez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frndmg/compai',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
