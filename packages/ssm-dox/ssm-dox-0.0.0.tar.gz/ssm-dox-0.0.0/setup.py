# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssm_dox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ssm-dox',
    'version': '0.0.0',
    'description': 'CLI tool for building and publishing SSM Documents.',
    'long_description': '# ssm-dox\n\nCLI tool for building and publishing SSM Documents.\n',
    'author': 'Kyle Finley',
    'author_email': 'kyle@finley.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ITProKyle/ssm-dox',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
