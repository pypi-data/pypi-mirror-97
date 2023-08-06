# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parachute']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'json5>=0.9.5,<0.10.0',
 'pymavlink>=2.4.14,<3.0.0',
 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['parachute = parachute.cli:cli']}

setup_kwargs = {
    'name': 'parachute',
    'version': '0.2.1',
    'description': 'A lifeline for ArduPilot craft.',
    'long_description': 'Parachute\n=========\n\nParachute is a swiss army knife for ArduPilot settings. It helps you quickly and\neasily back up all your parameters to a file (and restore them). It also lets\nyou get/set them, filter them, diff them, restore them or convert them to\nparameter files compatible with Mission Planner/QGroundControl.\n\n\nInstallation\n------------\n\nInstalling Parachute is simple. You can use `pipx` (recommended):\n\n```\n$ pipx install parachute\n```\n\nOr `pip` (less recommended):\n\n```\n$ pip install parachute\n```\n\n\nUsage\n-----\n\nParachute is called like so:\n\n```\n$ parachute backup <craft name>\n```\n\nFor example:\n\n```\n$ parachute backup Mini-Drak\n```\n\nTo restore:\n\n```\n$ parachute restore backup.chute\n```\n\n\nConversion\n----------\n\nYou can also convert a Parachute file to a file compatible with Mission Planner or QGroundControl:\n\n```\n$ parachute convert qgc Mini-Drak_2021-03-02_02-29.chute Mini-Drak.params\n```\n\n\nFiltering\n---------\n\nYou can filter parameters based on a regular expression:\n\n```\n$ parachute filter "serial[123]_" Mini-Drak_2021-03-02_02-29.chute filtered.chute\n```\n\nSince all parameter names are uppercase, the regex is case-insensitive, for convenience.\n\nYou can also filter when converting:\n\n```\n$ parachute convert --filter=yaw mp Mini-Drak_2021-03-02_02-29.chute -\n```\n\n\nComparing\n---------\n\nYou can compare parameters in a backup with parameters on the craft:\n\n```\n$ parachute compare backup.chute\n```\n\n\nGetting/setting\n---------------\n\nYou can get and set parameters:\n\n```\n$ parachute get BATT_AMP_OFFSET BATT_AMP_PERVLT\n```\n\n```\n$ parachute set BATT_AMP_OFFSET=-0.0135 BATT_AMP_PERVLT=63.8826\n```\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/stavros/parachute',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
