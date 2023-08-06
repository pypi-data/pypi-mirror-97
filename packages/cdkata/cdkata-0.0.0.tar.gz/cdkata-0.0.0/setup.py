# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdkata']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.22,<2.0.0', 'fire>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['cdkata = cdkata.cli:main']}

setup_kwargs = {
    'name': 'cdkata',
    'version': '0.0.0',
    'description': 'CDKata',
    'long_description': '# cdkata\nNot really sure what this is - Stay tuned.\n',
    'author': 'Mark Beacom',
    'author_email': 'm@beacom.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mbeacoom.github.io/cdkata/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
