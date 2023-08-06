#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click

from ._bookmark_cli import bookmark
from ._branch_cli import branch
from ._config_cli import config
from ._container_cli import container
from ._database_cli import database
from ._environment_cli import environment
from ._snapshot_cli import snapshot
from ._template_cli import template

__version__ = "1.1.0"


@click.group()
@click.version_option(version=__version__, prog_name="dxi")
def dxi():
    """
    Delphix CLI that makes it easier to
    integrate Delphix into automated workflows
    """


# Adding snapshot as sub-group-command of dxi
dxi.add_command(snapshot)

# Adding snapshot as sub-group-command of dxi
dxi.add_command(database)

# Adding environment as sub-group-command of dxi
dxi.add_command(environment)

# Adding branch as sub-group-command of dxi
dxi.add_command(branch)

# Adding bookmark as sub-group-command of dxi
dxi.add_command(bookmark)

# Adding container as sub-group-command of dxi
dxi.add_command(container)

# Adding template as sub-group-command of dxi
dxi.add_command(template)

# Adding config as sub-group-command of dxi
dxi.add_command(config)

if __name__ == "__main__":
    dxi()
