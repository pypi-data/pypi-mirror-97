# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['speedtest_manager']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.7.0,<4.0.0',
 'SQLAlchemy>=1.3.23,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2021.1,<2022.0',
 'tinydb>=4.3.0,<5.0.0',
 'tinyrecord>=0.2.0,<0.3.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['speedtest-client = speedtest_manager.client:main',
                     'speedtest-manager = speedtest_manager.manager:main']}

setup_kwargs = {
    'name': 'speedtest-manager',
    'version': '0.1.3',
    'description': "Manager service that uses Ookla's Speedtest CLI utility to perform measurements on the local network.",
    'long_description': None,
    'author': 'Thiago Marback',
    'author_email': 'tmarback@sympho.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
