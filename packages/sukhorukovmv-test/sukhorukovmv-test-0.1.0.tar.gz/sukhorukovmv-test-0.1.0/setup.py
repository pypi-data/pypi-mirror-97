# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['sukhorukovmv-test', 'sukhorukovmv-test.scripts']

package_data = \
{'': ['*']}

install_requires = \
['kubernetes>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['sukhorukovmv = python_package:start']}

setup_kwargs = {
    'name': 'sukhorukovmv-test',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Maksim Sukhorukov',
    'author_email': 'maksim.sukhorukov@firstlinesoftware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
