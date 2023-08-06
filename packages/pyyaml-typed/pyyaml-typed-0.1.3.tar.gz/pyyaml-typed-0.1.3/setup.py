# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyaml']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3,<6.0']

setup_kwargs = {
    'name': 'pyyaml-typed',
    'version': '0.1.3',
    'description': 'PyYAML dumper/loader using field descriptions in class comments',
    'long_description': '# pyyaml-typed\n[![Build Status](https://travis-ci.org/outcatcher/pyyaml-typed.svg?branch=master)](https://travis-ci.org/outcatcher/pyyaml-typed)\n[![codecov](https://codecov.io/gh/outcatcher/pyyaml-typed/branch/master/graph/badge.svg)](https://codecov.io/gh/outcatcher/pyyaml-typed)\n[![PyPI version](https://img.shields.io/pypi/v/pyyaml-typed.svg)](https://pypi.org/project/pyyaml-typed/)\n![GitHub](https://img.shields.io/github/license/outcatcher/pyyaml-typed)\n\nLibrary providing `dump` and `load` functions for pyyaml supporting `go-yaml`-like\ndescription of yaml fields as class comments\n\nDataclasses and named tuples can be used without defining field names.\nField in comment for them will override default class field name\n\nExample:\n\n```python3\nfrom tyaml import dump\n\n@dataclass\nclass Something:\n    my_fld_1: int\n    # or use `yaml:` comment to rename\n    field2: str  # yaml: my_fld_2\n    \noutput = dump([Something(1, "that\'s"), Something(2, "nice")])\n```\n\nwill create yaml:\n```yaml\n- my_fld_1: 1\n  my_fld_2: "that\'s"\n- my_fld_1: 2\n  my_fld_2: "nice"\n```\n\nand in the opposite direction: \n```python\nfrom typing import List\n\nfrom tyaml import load\n\nloaded = load(yml_str, List[Something])\nloaded == [Something(1, "that\'s"), Something(2, "nice")]\n```\n',
    'author': 'Anton Kachurin',
    'author_email': 'katchuring@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/outcatcher/pyyaml-typed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
