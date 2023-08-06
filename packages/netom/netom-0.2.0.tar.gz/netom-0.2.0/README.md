
# netom

[![PyPI](https://img.shields.io/pypi/v/netom.svg?maxAge=3600)](https://pypi.python.org/pypi/netom)
[![PyPI](https://img.shields.io/pypi/pyversions/netom.svg?maxAge=3600)](https://pypi.python.org/pypi/netom)
[![Tests](https://github.com/20c/netom/workflows/tests/badge.svg)](https://github.com/20c/netom)
[![Codecov](https://img.shields.io/codecov/c/github/20c/netom/master.svg?maxAge=3600)](https://codecov.io/github/20c/netom)

Network object models


### Development

Install (poetry)[https://python-poetry.org/]

```sh
poetry install
```

Testing:
```sh
poetry run pytest -v -rxs --cov-report term-missing --cov=src/netom/ tests/
```

Rendering:

```sh
poetry run netom render bgp_neighbors netom0 bird1-0 tests/data/config/bgp/neighbors.yml
```

### Template filters

`make_variable_name`: Makes value into a name safe to use as a variable name. Changes spaces, punctuation, etc into `_`

`ip_version`: returns IP version of passed value (returns either 4 or 6).


### License

Copyright 2018-2021 20C, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this softare except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
