# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sure_shot_static']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0', 'boto3>=1.17.21,<2.0.0', 'python-magic>=0.4.22,<0.5.0']

entry_points = \
{'console_scripts': ['sure-shot-static = '
                     'sure_shot_static.shake_your_rump:shake_your_rump']}

setup_kwargs = {
    'name': 'sure-shot-static',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'doubleO8',
    'author_email': 'wb008@hdm-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
