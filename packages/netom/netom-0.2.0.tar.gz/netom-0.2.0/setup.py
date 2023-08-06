# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['netom']

package_data = \
{'': ['*'],
 'netom': ['.github/workflows/*',
           'templates/netom0/*',
           'templates/netom0/bird1-0/bgp/*',
           'templates/netom0/junos-0/bgp/*',
           'templates/netom0/junos-set-0/bgp/*',
           'templates/netom0/sros-classic-0/bgp/*',
           'templates/netom0/sros-md-0/bgp/*',
           'templates/netom0/sros-md-fc-0/bgp/*']}

install_requires = \
['Jinja2>=2.10.1,<3.0.0',
 'confu>=1.7.1,<2.0.0',
 'munge>=1.1.0,<2.0.0',
 'tmpl>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['netom = netom.cli:main']}

setup_kwargs = {
    'name': 'netom',
    'version': '0.2.0',
    'description': 'network object models',
    'long_description': '\n# netom\n\n[![PyPI](https://img.shields.io/pypi/v/netom.svg?maxAge=3600)](https://pypi.python.org/pypi/netom)\n[![PyPI](https://img.shields.io/pypi/pyversions/netom.svg?maxAge=3600)](https://pypi.python.org/pypi/netom)\n[![Tests](https://github.com/20c/netom/workflows/tests/badge.svg)](https://github.com/20c/netom)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/netom/master.svg?maxAge=3600)](https://codecov.io/github/20c/netom)\n\nNetwork object models\n\n\n### Development\n\nInstall (poetry)[https://python-poetry.org/]\n\n```sh\npoetry install\n```\n\nTesting:\n```sh\npoetry run pytest -v -rxs --cov-report term-missing --cov=src/netom/ tests/\n```\n\nRendering:\n\n```sh\npoetry run netom render bgp_neighbors netom0 bird1-0 tests/data/config/bgp/neighbors.yml\n```\n\n### Template filters\n\n`make_variable_name`: Makes value into a name safe to use as a variable name. Changes spaces, punctuation, etc into `_`\n\n`ip_version`: returns IP version of passed value (returns either 4 or 6).\n\n\n### License\n\nCopyright 2018-2021 20C, LLC\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this softare except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
