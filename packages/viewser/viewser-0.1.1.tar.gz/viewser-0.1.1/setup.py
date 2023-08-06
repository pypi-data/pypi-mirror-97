# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viewser']

package_data = \
{'': ['*']}

install_requires = \
['environs>=9.3.1,<10.0.0',
 'fire>=0.4.0,<0.5.0',
 'pandas>=1.2.3,<2.0.0',
 'pyarrow>=3.0.0,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['viewser = viewser.cli:cli']}

setup_kwargs = {
    'name': 'viewser',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
