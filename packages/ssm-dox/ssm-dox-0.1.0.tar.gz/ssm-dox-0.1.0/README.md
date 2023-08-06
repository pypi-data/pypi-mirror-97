# ssm-dox

[![PyPi](https://img.shields.io/pypi/v/ssm-dox?style=flat)](https://pypi.org/project/ssm-dox/)
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/ssm-dox/badge/?version=latest)](https://ssm-dox.readthedocs.io/en/latest/?badge=latest)

CLI tool for building and publishing SSM Documents.

## What Is Dox?

**Dox** is a directory containing the source code of an SSM document.
Named for it's corresponding SSM Document, the directory contains the following:

- ``template.yaml`` or ``template.yml`` file **[REQUIRED]**
- ``README.md`` file describing the SSM Document
- external files to be included in the SSM Document (e.g. shell or PowerShell scripts)

## Why Use Dox?

Using **Dox** to write an SSM Document allows for scripts and other items to be linted and tested outside of the SSM Document.
This enables CI/CD pipelines to easily validate the code before it gets deployed to AWS.
