# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datar',
 'datar.base',
 'datar.datar',
 'datar.datasets',
 'datar.dplyr',
 'datar.stats',
 'datar.tibble',
 'datar.tidyr',
 'datar.utils']

package_data = \
{'': ['*'], 'datar': ['core/*']}

install_requires = \
['modkit', 'pandas>=1.2,<2.0', 'pipda']

setup_kwargs = {
    'name': 'datar',
    'version': '0.0.0',
    'description': 'Probably the closest port of tidyr, dplyr and tibble in python',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
