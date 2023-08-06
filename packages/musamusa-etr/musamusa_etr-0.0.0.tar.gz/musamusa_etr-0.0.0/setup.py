# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa_etr']

package_data = \
{'': ['*']}

install_requires = \
['musamusa-errors>=0.0.8,<0.0.9', 'musamusa-fal>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'musamusa-etr',
    'version': '0.0.0',
    'description': 'Easy To Read text format file',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
