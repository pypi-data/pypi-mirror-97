"""Publish SSM Documents from ``DOCUMENTS_DIRECTORY`` to an S3 ``BUCKET``.

If DOCUMENTS_DIRECTORY (absolute or relative) is omitted, ``./ssm_documents`` is used.

.. rubric:: Usage
.. code-block:: shell

  $ ssm-dox publish [OPTIONS] BUCKET [DOCUMENTS_DIRECTORY]

.. rubric:: Options
.. code-block:: text

  -p, --prefix TEXT  prefix to append to S3 Object key  [default: dev]
  --profile TEXT     AWS profile name
  --region TEXT      AWS region where the bucket is located
  -h, --help         Show this message and exit.

.. rubric:: Example
.. code-block:: shell

  $ ssm-dox publish example-bucket
  $ ssm-dox publish example-bucket ./ssm_documents --prefix latest
  $ ssm-dox publish example-bucket ./ssm_documents --region us-east-1

"""
import logging
from pathlib import Path
from typing import Optional

import boto3
import click

from ...constants import DOCUMENTS_DIR
from ...finder import Finder
from .utils import click_directory

LOGGER = logging.getLogger(__name__)


@click.command("publish", short_help="publish documents")
@click.argument("bucket", required=True)
@click.argument("documents_directory", callback=click_directory, default=DOCUMENTS_DIR)
@click.option(
    "-p",
    "--prefix",
    default="dev",
    help="prefix to append to S3 Object key",
    show_default=True,
)
@click.option("--profile", default=None, help="AWS profile name")
@click.option("--region", default=None, help="AWS region where the bucket is located")
def publish(
    bucket: str,
    documents_directory: Path,
    *,
    prefix: Optional[str] = None,
    profile: Optional[str] = None,
    region: Optional[str] = None,
) -> None:
    """Publish SSM Documents from DOCUMENTS_DIRECTORY to an S3 ``BUCKET``.

    If DOCUMENTS_DIRECTORY (absolute or relative) is omitted, ./ssm_documents is used.

    """
    finder = Finder(root_dir=documents_directory)
    session = boto3.Session(profile_name=profile, region_name=region)  # type: ignore
    s3_client = session.client("s3")
    for doc in finder.documents:
        doc.publish(s3_client, bucket=bucket, prefix=prefix)
