# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dustpan']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dustpan = dustpan.__main__:main']}

setup_kwargs = {
    'name': 'dustpan',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `dustpan`\n\n[![pypi version](https://img.shields.io/pypi/v/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)\n[![downloads](https://pepy.tech/badge/dustpan)](https://pepy.tech/project/dustpan)\n[![build status](https://github.com/dawsonbooth/dustpan/workflows/build/badge.svg)](https://github.com/dawsonbooth/dustpan/actions?workflow=build)\n[![python versions](https://img.shields.io/pypi/pyversions/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)\n[![format](https://img.shields.io/pypi/format/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)\n[![license](https://img.shields.io/pypi/l/dustpan.svg?style=flat)](https://github.com/dawsonbooth/dustpan/blob/master/LICENSE)\n\n## Description\n\nThis is a short or long textual description of the package.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npython -m pip install dustpan\n```\n\n## Usage\n\nThe following is an example usage of the package:\n\n```python\nfrom foo import bar\n\nprint("Ok here we go")\n\ntry:\n    bar()\nexcept:\n    print("Ah good effort")\n```\n\nSome info about calling the program.\n\n```bash\npython whatever.py > out.txt\n```\n\nThen some output (console or file whatever)\n\n```txt\nOutput here I guess\n```\n\nFeel free to [check out the docs](https://dawsonbooth.github.io/dustpan/) for more information.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/dustpan',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
