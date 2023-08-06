# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssm_dox',
 'ssm_dox._cli',
 'ssm_dox._cli.commands',
 'ssm_dox.models',
 'ssm_dox.models.main_steps']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=4.1,<5.3',
 'boto3>=1.17.23,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'coloredlogs>=15.0,<16.0',
 'pydantic>=1.8.1,<2.0.0']

extras_require = \
{'docs': ['readthedocs-sphinx-search>=0.1.0,<0.2.0',
          'Sphinx>=3.5.2,<4.0.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0',
          'toml>=0.10.2,<0.11.0']}

entry_points = \
{'console_scripts': ['ssm-dox = ssm_dox._cli.main:cli']}

setup_kwargs = {
    'name': 'ssm-dox',
    'version': '0.1.0',
    'description': 'CLI tool for building and publishing SSM Documents.',
    'long_description': "# ssm-dox\n\n[![PyPi](https://img.shields.io/pypi/v/ssm-dox?style=flat)](https://pypi.org/project/ssm-dox/)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)\n[![Documentation Status](https://readthedocs.org/projects/ssm-dox/badge/?version=latest)](https://ssm-dox.readthedocs.io/en/latest/?badge=latest)\n\nCLI tool for building and publishing SSM Documents.\n\n## What Is Dox?\n\n**Dox** is a directory containing the source code of an SSM document.\nNamed for it's corresponding SSM Document, the directory contains the following:\n\n- ``template.yaml`` or ``template.yml`` file **[REQUIRED]**\n- ``README.md`` file describing the SSM Document\n- external files to be included in the SSM Document (e.g. shell or PowerShell scripts)\n\n## Why Use Dox?\n\nUsing **Dox** to write an SSM Document allows for scripts and other items to be linted and tested outside of the SSM Document.\nThis enables CI/CD pipelines to easily validate the code before it gets deployed to AWS.\n",
    'author': 'Kyle Finley',
    'author_email': 'kyle@finley.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ITProKyle/ssm-dox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
