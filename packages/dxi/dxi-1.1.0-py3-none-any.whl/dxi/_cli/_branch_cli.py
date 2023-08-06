#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.branch.dxi_branch import DXIBranch
from dxi.branch.dxi_branch import DXIBranchConstants


@click.group()
def branch():
    """
    Group command for branch operations
    """
    pass


@branch.command()
@click.option(
    "--engine",
    default=DXIBranchConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIBranchConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIBranchConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIBranchConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIBranchConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIBranchConstants.LOG_FILE_PATH,
)
@click.option(
    "--branchname", required=True, help="Name of the branch to delete"
)
def delete(
    engine, single_thread, parallel, poll, config, log_file_path, branchname
):
    """
    Delete a branch by name
    """
    env_obj = DXIBranch(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.delete(branch_name=branchname))


@branch.command()
@click.option(
    "--branchname", required=True, help="Name of the branch to activate"
)
@click.option(
    "--containername",
    required=True,
    help="Name of the parent container for the branch",
)
@click.option(
    "--engine",
    default=DXIBranchConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIBranchConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIBranchConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIBranchConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIBranchConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIBranchConstants.LOG_FILE_PATH,
)
def activate(
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    branchname,
    containername,
):
    """
    Activate a branch by name
    """
    env_obj = DXIBranch(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(
        env_obj.activate(branch_name=branchname, container_name=containername)
    )


@branch.command()
@click.option(
    "--engine",
    default=DXIBranchConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIBranchConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIBranchConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIBranchConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIBranchConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIBranchConstants.LOG_FILE_PATH,
)
def list(engine, single_thread, parallel, poll, config, log_file_path):
    """
    List all branches on an engine
    """
    env_obj = DXIBranch(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.list())


@branch.command()
@click.option(
    "--branchname", default=None, required=True, help="Name of the Branch"
)
@click.option(
    "--containername",
    default=None,
    required=True,
    help="Name of the Self Service Container",
)
@click.option(
    "--templatename", default=None, help="Name of the Self Service Template"
)
@click.option(
    "--bookmarkname",
    default=None,
    help="Name of the bookmark to create the branch",
)
@click.option(
    "--timestamp", default=None, help="Timestamp to create the branch"
)
@click.option(
    "--engine", help="Name of the engine", default=DXIBranchConstants.ENGINE_ID
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=DXIBranchConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=DXIBranchConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=DXIBranchConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIBranchConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIBranchConstants.LOG_FILE_PATH,
)
def create(
    branchname,
    containername,
    templatename,
    bookmarkname,
    timestamp,
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
):
    """
    Create a new Branch
    """
    env_obj = DXIBranch(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(
        env_obj.create(
            branch_name=branchname,
            container_name=containername,
            template_name=templatename,
            bookmark_name=bookmarkname,
            timestamp=timestamp,
        )
    )


if __name__ == "__main__":
    activate()
