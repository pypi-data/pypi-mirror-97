# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytire']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytire',
    'version': '0.2.1',
    'description': 'Python library to handle tire attributes.',
    'long_description': '# pytire\n[![Documentation Status](https://readthedocs.org/projects/pytire/badge/?version=latest)](https://pytire.readthedocs.io/en/latest/?badge=latest)\n![Build Status](https://img.shields.io/github/workflow/status/girotobial/pytire/test)\n[![PyPI Version](https://img.shields.io/pypi/v/pytire)](https://pypi.org/project/pytire/)\n[![Licence](https://img.shields.io/github/license/girotobial/pytire)](https://github.com/girotobial/pytire/blob/main/LICENSE)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nA library to make interpreting tire attributes and calculations easier.\n\n### Table of Contents\n  * [Table of Contents](#table-of-contents)\n  * [Getting Started](#getting-started)\n  * [Dev Setup](#dev-setup)\n## Getting Started\nTo use this library install it via pip\n\n```sh\n$ pip install pytire\n```\n\nimport into python\n```python\nfrom pytire import Tire\n\ntire = Tire("34x10.75-16")\n```\n[The Docs are here.](https://pytire.readthedocs.io/en/latest/)\n## Dev Setup\n\nClone from github\n```\n$ git clone \n```\n\nInstall using poetry\n```sh\n$ poetry install\n```\nset up pre-commit\n```sh\n$ pre-commit install\n```\n\nAlternatively use the dev container.\n',
    'author': 'girotobial',
    'author_email': 'abrobinson1907@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/girotobial/pytire',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
