# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyrgbd']

package_data = \
{'': ['*']}

install_requires = \
['cffi>=1.15.1,<2.0.0',
 'numpy>=1.23.2,<2.0.0',
 'opencv-python>=4.6.0,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'vedo>=2022.2.3,<2023.0.0']

setup_kwargs = {
    'name': 'pyrgbd',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Hanseul Jun',
    'author_email': 'hanseul@telegie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
