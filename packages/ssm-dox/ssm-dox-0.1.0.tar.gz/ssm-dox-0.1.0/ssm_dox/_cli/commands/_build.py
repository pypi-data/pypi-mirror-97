"""Build SSM Documents from Dox in ``DOX_DIRECTORY``.

If ``DOX_DIRECTORY`` (absolute or relative) is omitted, ``./dox`` is used.

.. rubric:: Usage
.. code-block:: shell

  $ ssm-dox build [OPTIONS] [DOX_DIRECTORY]

.. rubric:: Options
.. code-block:: text

  -o, --output TEXT  path where built files should be placed
                     [default: ./ssm_documents]

.. rubric:: Example
.. code-block:: shell

  $ ssm-dox build
  $ ssm-dox build ./dox
  $ ssm-dox build ./dox --output ./ssm_documents

"""
from pathlib import Path

import click

from ...constants import DOCUMENTS_DIR, DOX_DIR
from ...finder import Finder
from .utils import click_directory


@click.command("build", short_help="build dox")
@click.argument("dox_directory", callback=click_directory, default=DOX_DIR)
@click.option(
    "-o",
    "--output",
    callback=click_directory,
    default=DOCUMENTS_DIR,
    help="path where built files should be placed",
    show_default=True,
)
def build(dox_directory: Path, output: Path) -> None:
    """Build SSM Documents from Dox in DOX_DIRECTORY.

    If DOX_DIRECTORY (absolute or relative) is omitted, ./dox is used.

    """
    finder = Finder(root_dir=dox_directory)
    for dox in finder.dox:
        dox.build(output)
