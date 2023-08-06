# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prediktor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0', 'pandas>=1.0,<2.0']

setup_kwargs = {
    'name': 'prediktor',
    'version': '0.1.0',
    'description': 'Universal prediction interface for deploying ML models',
    'long_description': None,
    'author': 'mavillan',
    'author_email': 'mavillan@spikelab.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
