# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iiintent']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iiintent',
    'version': '0.42.10',
    'description': 'Immuring Iniquitious Intent',
    'long_description': None,
    'author': 'Scott McCallum',
    'author_email': 'cto@iiintent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
