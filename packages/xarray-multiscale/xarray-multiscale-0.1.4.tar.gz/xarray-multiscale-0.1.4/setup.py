# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xarray_multiscale', 'xarray_multiscale.metadata']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.11.0,<0.12.0',
 'dacite>=1.6.0,<2.0.0',
 'dask',
 'mypy>=0.790,<0.791',
 'numpy>=1.19.4,<2.0.0',
 'scipy>=1.5.4,<2.0.0',
 'xarray>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'xarray-multiscale',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Davis Vann Bennett',
    'author_email': 'davis.v.bennett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
