# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isabelle_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'isabelle-client',
    'version': '0.1.1',
    'description': 'A client to Isabelle proof assistant server',
    'long_description': '[![PyPI version](https://badge.fury.io/py/isabelle-client.svg)](https://badge.fury.io/py/isabelle-client) [![CircleCI](https://circleci.com/gh/inpefess/isabelle-client.svg?style=svg)](https://circleci.com/gh/inpefess/isabelle-client) [![Documentation Status](https://readthedocs.org/projects/isabelle-client/badge/?version=latest)](https://isabelle-client.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/inpefess/isabelle-client/branch/master/graph/badge.svg)](https://codecov.io/gh/inpefess/isabelle-client)\n\n# Isabelle Client\n\nA client for [Isabelle](https://isabelle.in.tum.de) server. For more information about the server see part 4 of [the Isabelle system manual](https://isabelle.in.tum.de/dist/Isabelle2021/doc/system.pdf).\n\nFor information on using this client see [documentation](https://isabelle-client.readthedocs.io).\n\n![video tutorial](https://github.com/inpefess/isabelle-client/blob/master/examples/tty.gif).\n\nIssues and PRs are welcome.\n',
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/isabelle-client',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
