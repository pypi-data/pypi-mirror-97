# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['cognite',
 'cognite.well_model',
 'cognite.well_model.client',
 'cognite.well_model.client.api',
 'cognite.well_model.client.utils']

package_data = \
{'': ['*']}

install_requires = \
['cognite-logger>=0.5.0,<0.6.0',
 'helpers>=0.2.0,<0.3.0',
 'nulltype>=2.3.1,<3.0.0',
 'numpy>=1.18.1,<2.0.0',
 'oauthlib>=3.1.0,<4.0.0',
 'pandas>=1.0.1,<2.0.0',
 'pydantic>=1.8,<2.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'cognite-wells-sdk',
    'version': '0.4.3',
    'description': '',
    'long_description': None,
    'author': 'Dylan Phelps',
    'author_email': 'dylan.phelps@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
