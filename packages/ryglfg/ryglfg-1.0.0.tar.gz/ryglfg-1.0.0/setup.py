# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ryglfg']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.0b3,<2.0.0',
 'fastapi-cloudauth>=0.3.0,<0.4.0',
 'fastapi>=0.63.0,<0.64.0',
 'psycopg2>=2.8.6,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'royalnet>=6.0.2,<7.0.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'ryglfg',
    'version': '1.0.0',
    'description': 'The "Looking For Group" service of the RYG community',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
