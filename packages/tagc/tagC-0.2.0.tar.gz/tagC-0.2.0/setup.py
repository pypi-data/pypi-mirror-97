# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagc']

package_data = \
{'': ['*']}

install_requires = \
['dash>=1.16.2,<2.0.0',
 'fire>=0.3.1,<0.4.0',
 'kaleido>=0.2.1,<0.3.0',
 'openpyxl>=3.0.6,<4.0.0',
 'pandas>=1.1.3,<2.0.0',
 'plotly>=4.11.0,<5.0.0',
 'requests>=2.24.0,<3.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'toolz>=0.11.1,<0.12.0',
 'torch>=1.7.0,<2.0.0',
 'tqdm>=4.50.1,<5.0.0',
 'transformers==3.5.1',
 'wheel>=0.35.1,<0.36.0']

setup_kwargs = {
    'name': 'tagc',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Kiyoshi Mu',
    'author_email': 'mooyewtsing@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
