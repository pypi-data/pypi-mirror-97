# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iiintent']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'faker>=6.5.2,<7.0.0',
 'itsdangerous>=1.1.0,<2.0.0',
 'lxml>=4.6.2,<5.0.0',
 'mitmproxy==5.3',
 'pysimplegui>=4.35.0,<5.0.0']

setup_kwargs = {
    'name': 'iiintent',
    'version': '0.42.11',
    'description': 'Immuring Iniquitious Intent',
    'long_description': None,
    'author': 'Scott McCallum',
    'author_email': 'cto@iiintent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
