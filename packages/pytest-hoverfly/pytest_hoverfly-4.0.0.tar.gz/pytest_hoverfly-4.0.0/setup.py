# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_hoverfly']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.2.0,<5.0.0',
 'pytest>=5.0',
 'requests>=2.22.0,<3.0.0',
 'typing_extensions>=3.7.4,<4.0.0']

entry_points = \
{'pytest11': ['hoverfly = pytest_hoverfly.pytest_hoverfly']}

setup_kwargs = {
    'name': 'pytest-hoverfly',
    'version': '4.0.0',
    'description': 'Simplify working with Hoverfly from pytest',
    'long_description': None,
    'author': 'Devops team',
    'author_email': 'devops@team.wrike.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.wrke.in/ops/pytset-hoverfly',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
