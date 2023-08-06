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
    'version': '4.0.1',
    'description': 'Simplify working with Hoverfly from pytest',
    'long_description': "A helper for working with [Hoverfly](https://hoverfly.readthedocs.io/en/latest/) from `pytest`.\n\n### Installation\n`pip install pytest-hoverfly`\n\nor\n\n`poetry add pytest-hoverfly --dev`\n\n\n### Usage\nThere are two use cases: to record a new test and to use recordings.\n\n#### Prerequisites\nCreate a directory to store simulation files. Pass `--hoverfly-simulation-path` option \nwhen calling `pytest`. The path may be absolute or relative to your `pytest.ini` file.\nE.g. if you have a structure like this:\n```\n├── myproject\n    ├── ...\n├── pytest.ini\n└── tests\n    ├── conftest.py\n    ├── simulations\n```\n\nThen put this in you pytest.ini:\n```\n[pytest]\naddopts =\n    --hoverfly-simulation-path=tests/simulations\n```\n\n#### How to record a test\n```python\nfrom pytest_hoverfly import hoverfly\nimport requests\n\n\n@hoverfly('my-simulation-file', record=True)\ndef test_google_with_hoverfly():\n    assert requests.get('https://google.com').status_code == 200\n```\n\nWrite a test. Decorate it with `@hoverfly`, specifying a name of a file to save the simulation to. \nRun the test. A Hoverfly container will be created, and  `HTTP_PROXY` and `HTTPS_PROXY` env vars \nwill be set to point to this container. After test finishes, the resulting simulation will \nbe exported from Hoverfly and saved to a file you specified. After test session ends, Hoverfly\ncontainer will be destroyed (unless `--hoverfly-reuse-container` is passed to pytest).\n\nThis will work for cases when a server always returns the same response for the same\nrequest. If you need to work with stateful endpoints (e.g. wait for Teamcity build\nto finish), use `@hoverfly('my-simulation, record=True, stateful=True)`. See \n[Hoverfly docs](https://docs.hoverfly.io/en/latest/pages/tutorials/basic/capturingsequences/capturingsequences.html)\nfor details.\n\n#### How to use recordings\nRemove `record` parameter. That's it. When you run the test, it will create a container \nwith Hoverfly, upload your simulation into it, and use it instead of a real service.\n\n```python\nfrom pytest_hoverfly import hoverfly\nimport requests\n\n\n@hoverfly('my-simulation-file')\ndef test_google_with_hoverfly():\n    assert requests.get('https://google.com').status_code == 200\n```\n\nCaveat: if you're using an HTTP library other than `aiohttp` or `requests` you need to\ntell it to use Hoverfly as HTTP(S) proxy and to trust Hoverfly's certificate. See\n`_patch_env` fixture for details on how it's done for `aiohttp` and `requests`.\n\n#### How to re-record a test\nAdd `record=True` again, and run the test. The simulation file will be overwritten.\n",
    'author': 'Devops team',
    'author_email': 'devops@team.wrike.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wrike/pytest-hoverfly',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
