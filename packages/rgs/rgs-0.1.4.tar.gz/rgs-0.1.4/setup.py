# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rgs', 'rgs.mndrpy', 'rgs.pmaps', 'rgs.ribbons', 'rgs.slimtree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rgs',
    'version': '0.1.4',
    'description': 'A small package to display and manipulate random geometry structures like pairings, meanders, triangulations and tilings.',
    'long_description': '# RandomGeometricStructures\nA collection of various function to draw and analyze random geometric structures (like pairings, tilings etc.)\n',
    'author': 'Vladislav Kargin',
    'author_email': 'slavakargin@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
