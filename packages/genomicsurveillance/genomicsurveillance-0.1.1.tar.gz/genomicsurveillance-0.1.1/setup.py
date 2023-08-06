# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genomicsurveillance', 'genomicsurveillance.data']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0', 'numpyro>=0.5.0,<0.6.0', 'pandas>=1.2.3,<2.0.0']

extras_require = \
{'docs': ['sphinx>=3,<4'],
 'geopandas': ['geopandas>=0.9.0,<0.10.0'],
 'matplotlib': ['matplotlib>=3.3.4,<4.0.0'],
 'uk-covid19': ['uk-covid19>=1.2.0,<2.0.0']}

setup_kwargs = {
    'name': 'genomicsurveillance',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Harald Vohringer',
    'author_email': 'harald.voeh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
