import sys

import click

from . import config as g2t_config
from . import core


@click.command()
@click.option("-c", "--config", help="Open up configuration file.", is_flag=True)
@click.option(
    "--dry-run",
    help="Show what time entries will be uploaded without actually uploading them.",
    is_flag=True
)
def main(config, dry_run):
    if config:
        g2t_config.open()
        return

    core.setup()
    core.upload_entries(dry_run=dry_run)


if __name__ == "__main__":
    main(sys.argv[1:])
