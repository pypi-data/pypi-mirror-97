# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moss', 'moss.ems', 'moss.ems.utilities']

package_data = \
{'': ['*']}

install_requires = \
['anytree>=2.8.0,<3.0.0', 'requests>=2.18.0,<3.0.0']

extras_require = \
{':python_version < "3.5"': ['typing>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'moss-emspy',
    'version': '1.0.2',
    'description': 'Package to interact with MOSS WEGA-EMS',
    'long_description': '# MOSS emspy\n\n## Description\n\nThis is the Python SDK to interact with [M.O.S.S. Computer Grafik Systeme GmbH](https://www.moss.de/wega/) WEGA-EMS\n\n## Installation\n\nThis package kann be installed using pip\n\n```shell\npython -m pip install moss_emspy\n```\n\n## Usage\n\n```python\nmy_service = Service("http://localhost:8080/wega-ems/",\n            username="Test",\n            password="Test")\nmy_service.projects\n```\n',
    'author': 'M.O.S.S.Computer Grafik Systeme GmbH',
    'author_email': 'develop@moss.de',
    'maintainer': 'M.O.S.S.Computer Grafik Systeme GmbH',
    'maintainer_email': 'develop@moss.de',
    'url': 'https://www.moss.de/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
