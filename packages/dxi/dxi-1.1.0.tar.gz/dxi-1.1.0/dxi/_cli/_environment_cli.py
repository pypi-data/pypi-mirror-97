#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click

from dxi._lib.util import boolean_based_system_exit
from dxi.environment.dxi_environment import DXIEnvironment
from dxi.environment.dxi_environment import EnvironmentConstants


@click.group()
def environment():
    """
    Group command for environment operations
    """
    pass


@environment.command()
@click.option(
    "--engine",
    default=EnvironmentConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
@click.option("--oldhost", help="Old IP or HostName of the environment")
@click.option("--newhost", help="New IP or HostName of the environment")
def updatehost(
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
    oldhost,
    newhost,
):
    """
    Update an environment's IP address
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.updatehost(old_host=oldhost, new_host=newhost))


@environment.command()
@click.option(
    "--engine",
    default=EnvironmentConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
@click.option(
    "--envname", required=True, help="Name of the environment to enable"
)
def delete(
    engine, single_thread, parallel, poll, config, log_file_path, envname
):
    """
    Delete an environment by name
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.delete(env_name=envname))


@environment.command()
@click.option(
    "--engine",
    default=EnvironmentConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
@click.option(
    "--envname", required=True, help="Name of the environment to enable"
)
def enable(
    engine, single_thread, parallel, poll, config, log_file_path, envname
):
    """
    Enable an environment by name
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.enable(env_name=envname))


@environment.command()
@click.option(
    "--engine",
    default=EnvironmentConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
@click.option(
    "--envname", required=True, help="Name of the environment to disable"
)
def disable(
    engine, single_thread, parallel, poll, config, log_file_path, envname
):
    """
    Disable an environment by name
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.disable(env_name=envname))


@environment.command()
@click.option(
    "--engine",
    default=EnvironmentConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
@click.option(
    "--envname", required=True, help="Name of the environment to refresh"
)
def refresh(
    engine, single_thread, parallel, poll, config, log_file_path, envname
):
    """
    Refresh an environment by name
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.refresh(env_name=envname))


@environment.command()
@click.option(
    "--engine",
    default=EnvironmentConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
def list(engine, single_thread, parallel, poll, config, log_file_path):
    """
    List all environments on an engine
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.list())


@environment.command()
@click.option(
    "--envname", required=True, help="Name of the environment to add"
)
@click.option(
    "--envtype",
    required=True,
    default=EnvironmentConstants.TYPE,
    help="Type of the environment [ unix or windows ]",
)
@click.option("--engine", default=EnvironmentConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=EnvironmentConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=EnvironmentConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=EnvironmentConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=EnvironmentConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=EnvironmentConstants.LOG_FILE_PATH,
)
@click.option(
    "--hostip",
    help="IP address or Hostname of the environment",
    default=EnvironmentConstants.HOSTIP,
)
@click.option(
    "--toolkitdir",
    help="Directory on the Unix/Linux environment "
    "to download Delphix Toolkit",
    default=None,
)
@click.option(
    "--username", help="Delphix OS user on the host environment", default=None
)
@click.option("--password", help="Delphix OS user password", default=None)
@click.option(
    "--connectorenvname",
    help="Name of the environment on which "
    " Windows connector is installed and running",
    default=None,
)
@click.option("--asedbusername", help="ASE DB username", default=None)
@click.option("--asedbpassword", help="ASE DB user's password", default=None)
def add(
    envname,
    envtype,
    hostip,
    toolkitdir,
    connectorenvname,
    username,
    password,
    asedbusername,
    asedbpassword,
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
):
    """
    Add an environment
    """
    env_obj = DXIEnvironment(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(env_obj.add(
        env_type=envtype,
        env_name=envname,
        host_ip=hostip,
        toolkit_dir=toolkitdir,
        connector_env_name=connectorenvname,
        username=username,
        password=password,
        ase_db_password=asedbpassword,
        ase_db_username=asedbusername,
    ))


if __name__ == "__main__":
    refresh()
