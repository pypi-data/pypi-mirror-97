#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.config.dxi_config import DXIConfig
from dxi.config.dxi_config import DXIConfigConstants


@click.group()
def config():
    """
    Group command for dxi config related operations
    """
    pass


# encrypt
@config.command()
@click.option(
    "--config-file",
    help="\b\nPath of the config file (including filename) \n"
    "that contains engine information",
    default=DXIConfigConstants.CONFIG,
)
@click.option(
    "--log-dir",
    help="\b Path to the log directory",
    default=DXIConfigConstants.LOG_FILE_PATH,
)
def encrypt(config_file, log_dir):
    """
    Encrypts username and password fields in config file.
    """
    temp_obj = DXIConfig(config=config_file, log_file_path=log_dir)
    boolean_based_system_exit(temp_obj.encrypt())


if __name__ == "__main__":
    encrypt()
