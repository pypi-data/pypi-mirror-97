# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canopy', 'canopy.templates']

package_data = \
{'': ['*']}

install_requires = \
['understory>=0.0.1-alpha.97,<0.0.2']

entry_points = \
{'web.apps': ['canopy = canopy:app']}

setup_kwargs = {
    'name': 'canopy-network',
    'version': '0.0.2a0',
    'description': 'A decentralized social network.',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
