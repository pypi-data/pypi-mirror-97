# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swc']

package_data = \
{'': ['*']}

install_requires = \
['bump2version>=1.0.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'pandas>=1.0.5,<2.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'requests>=2.24.0,<3.0.0',
 'tqdm>=4.46.1,<5.0.0']

setup_kwargs = {
    'name': 'swc',
    'version': '0.7.0',
    'description': 'Solar PV performance simulator',
    'long_description': None,
    'author': 'pesap',
    'author_email': 'pesapsanchez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
