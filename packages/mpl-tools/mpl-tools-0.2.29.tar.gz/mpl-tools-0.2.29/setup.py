# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpl_tools']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'mpl-tools',
    'version': '0.2.29',
    'description': 'Tools for working with matplotlib',
    'long_description': '# mpl-tools\n\n[![Travis](https://travis-ci.org/patricknraanes/mpl-tools.svg?branch=master)](https://travis-ci.org/patricknraanes/mpl-tools)\n[![Coveralls](https://coveralls.io/repos/github/patricknraanes/mpl-tools/badge.svg?branch=master)](https://coveralls.io/github/patricknraanes/mpl-tools?branch=master)\n[![Hits.dwyl](http://hits.dwyl.com/patricknraanes/mpl-tools.svg)](http://hits.dwyl.com/patricknraanes/mpl-tools)\n[![PyPI](https://badge.fury.io/py/mpl-tools.svg)](https://badge.fury.io/py/mpl-tools)\n[![PyPI - Downloads](https://img.shields.io/pypi/dw/mpl-tools)](https://pypi.org/project/mpl-tools/0.1.5/)\n\nThis package provides some tools to work with [Matplotlib](https://matplotlib.org/).\n\n## Installation\n\n#### Normal installation\n\n```sh\npip install mpl-tools\n```\n\n#### For development\n\n**On Linux**:\n`git clone <this repo> ; make install`\n\n**On Windows (or Linux)**:\nDownload & extract this repo.\nInstall [poetry](https://python-poetry.org/docs/#installation).\nRun `poetry install`.\n\n**Note**: The above will install *poetry*,\nwhich then installs the source and its dependencies\ninto an isolated *virtual environment*.\nTo add packages, you should *not* use `pip install`,\nbut *poetry*, e.g. `poetry add --dev somepackage`.\n\n<!-- markdownlint-disable-file header-increment -->\n',
    'author': 'patricknraanes',
    'author_email': 'patrick.n.raanes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/patricknraanes/mpl-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
