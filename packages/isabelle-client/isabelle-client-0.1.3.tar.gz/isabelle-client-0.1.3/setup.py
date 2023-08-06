# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isabelle_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'isabelle-client',
    'version': '0.1.3',
    'description': 'A client to Isabelle proof assistant server',
    'long_description': '[![PyPI version](https://badge.fury.io/py/isabelle-client.svg)](https://badge.fury.io/py/isabelle-client) [![CircleCI](https://circleci.com/gh/inpefess/isabelle-client.svg?style=svg)](https://circleci.com/gh/inpefess/isabelle-client) [![Documentation Status](https://readthedocs.org/projects/isabelle-client/badge/?version=latest)](https://isabelle-client.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/inpefess/isabelle-client/branch/master/graph/badge.svg)](https://codecov.io/gh/inpefess/isabelle-client)\n\n# Isabelle Client\n\nA client for [Isabelle](https://isabelle.in.tum.de) server. For more information about the server see part 4 of [the Isabelle system manual](https://isabelle.in.tum.de/dist/Isabelle2021/doc/system.pdf).\n\nFor information on using this client see [documentation](https://isabelle-client.readthedocs.io).\n\n# How to install\n\n```bash\npip install isabelle-client\n```\n\n# How to start Isabelle server\n\n```bash\nisabelle server > server.info\n```\n\nsince we\'ll need server info for connecting to it with this client. Or:\n\n```Python\nfrom isabelle_client.utils import start_isabelle_server\n\nserver_info, server_process = start_isabelle_server()\n``` \n\n# How to connect to the server\n\n```Python\nfrom isabelle_client.utils import get_isabelle_client\n\nisabelle = get_isabelle_client(server_info)\n```\n\n# How to send a command to the server\n\n```Python\nisabelle.session_build(dirs=["."], session="examples")\n```\n\nNote that this method returns only the last reply from the server.\n\n# How to log all replies from the server\n\nWe can add a standard Python logger to the client:\n\n```Python\nimport logging\n\nisabelle.logger = logging.getLogger()\nisabelle.logger.setLevel(logging.INFO)\nisabelle.logger.addHandler(logging.FileHandler("out.log"))\n```\n\nThen all replies from the server will go to the file ``out.log``.\n\n# Examples\n\nAn example of using this package is located in ``examples`` directory.\n\n# Video example\n\n![video tutorial](https://github.com/inpefess/isabelle-client/blob/master/examples/tty.gif).\n\n# Contributing\n\nIssues and PRs are welcome.\n',
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
