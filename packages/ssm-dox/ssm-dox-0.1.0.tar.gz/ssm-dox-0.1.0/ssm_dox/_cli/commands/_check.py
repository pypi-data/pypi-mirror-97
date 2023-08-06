"""Compare Dox in to SSM Documents to ensure the match.

If ``DOX_DIRECTORY`` (absolute or relative) is omitted, ``./dox`` is used.
If ``DOCUMENTS_DIRECTORY`` (absolute or relative) is omitted, ``./ssm_documents`` is used.

.. rubric:: Usage
.. code-block:: shell

  $ ssm-dox check [OPTIONS] [DOX_DIRECTORY] [DOCUMENTS_DIRECTORY]

.. rubric:: Example
.. code-block:: shell

  $ ssm-dox check
  $ ssm-dox check ./dox
  $ ssm-dox check ./dox ./ssm_documents

"""
import logging
from pathlib import Path

import click

from ...constants import DOCUMENTS_DIR, DOX_DIR
from ...exceptions import DocumentDrift
from ...finder import Finder
from .utils import click_directory

LOGGER = logging.getLogger(__name__)


@click.command("check", short_help="check dox")
@click.argument("dox_directory", callback=click_directory, default=DOX_DIR)
@click.argument("documents_directory", callback=click_directory, default=DOCUMENTS_DIR)
@click.pass_context
def check(ctx: click.Context, documents_directory: Path, dox_directory: Path) -> None:
    """Compare Dox in to SSM Documents to ensure the match.

    If DOX_DIRECTORY (absolute or relative) is omitted, ./dox is used.
    If DOCUMENTS_DIRECTORY (absolute or relative) is omitted, ./ssm_documents is used.

    """
    finder = Finder(root_dir=dox_directory)
    for dox in finder.dox:
        try:
            dox.check(documents_directory)
        except DocumentDrift as err:
            LOGGER.error(err)
            dox.diff(documents_directory)
            ctx.exit(1)
    LOGGER.info("all documents are up to date")
