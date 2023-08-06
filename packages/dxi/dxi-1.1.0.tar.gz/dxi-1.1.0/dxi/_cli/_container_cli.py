#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib.util import boolean_based_system_exit
from dxi.container.dxi_container import DXIContainer
from dxi.container.dxi_container import DXIContainerConstants


@click.group()
def container():
    """
    Creates, Lists, Removes a Self-Service Data Pod
    """
    pass


# List Command
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def list(engine, single_thread, config, log_file_path, poll):
    """
List all containers on a given engine
dxi container list
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.list())


# Create Container Command
@click.option(
    "--database",
    required=True,
    help=" Name of the child database(s) to use for the SS Container",
)
@click.option(
    "--template_name",
    required=True,
    help="Name of the JS Template to use for the container",
)
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def create(
    container_name,
    template_name,
    database,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
Create the SS container
dxi container create --template_name template --container_name container --database vOraCRM_BRKFIX
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.create(container_name, template_name, database)
    )


# Delete Container Command
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option(
    "--keep_vdbs",
    help="If set, deleting the container will not remove "
    "the underlying VDB(s)",
    default=False,
    is_flag=True,
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def delete(
    container_name,
    keep_vdbs,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
Deletes a container
dxi container delete --container_name container --keep_vdbs
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.delete(container_name, keep_vdbs=keep_vdbs)
    )


# Reset Container Command
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def reset(container_name, engine, single_thread, config, log_file_path, poll):
    """
Undo the last refresh or restore operation
dxi container reset --container_name container
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.reset(container_name))


# Reset Container Command
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def refresh(
    container_name, engine, single_thread, config, log_file_path, poll
):
    """
Refreshes a container
dxi container refresh --container_name container
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.refresh(container_name))


# Restore Container Command
@click.option(
    "--bookmark_name",
    required=True,
    help="Name of the JS Bookmark to restore the container",
)
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def restore(
    container_name,
    bookmark_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
Restores a container to a given JS bookmark
dxi container restore --container_name container --bookmark_name bookmark
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.restore(container_name, bookmark_name)
    )


# Lists hierarchy Command
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def connection_info(
    container_name, engine, single_thread, config, log_file_path, poll
):
    """
Show connection info
dxi container connection-info --container_name suiteCRM-Dev-DataPod
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(ss_container.connection_info(container_name))


# Add owner Command
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option(
    "--owner_name",
    required=True,
    help="Name of the JS Owner for the container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def add_owner(
    owner_name,
    container_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
Adds an owner to a container
dxi container add-owner --owner_name admin --container_name suiteCRM-Dev-DataPod
    """
    # print(owner_name, container_name)
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.add_owner(container_name, owner_name)
    )


# Delete owner Command
@click.option(
    "--container_name",
    required=True,
    help="Name of the SS Container",
)
@click.option(
    "--owner_name",
    required=True,
    help="Name of the JS Owner for the container",
)
@click.option("--engine", default=DXIContainerConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=False,
    is_flag=True,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=DXIContainerConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=DXIContainerConstants.LOG_FILE_PATH,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=DXIContainerConstants.POLL,
)
@container.command()
def remove_owner(
    container_name,
    owner_name,
    engine,
    single_thread,
    config,
    log_file_path,
    poll,
):
    """
Removes an owner from a container
dxi container remove-owner --owner_name admin --container_name suiteCRM-Dev-DataPod
    """
    ss_container = DXIContainer(
        engine=engine,
        single_thread=single_thread,
        config=config,
        log_file_path=log_file_path,
        poll=poll,
    )
    boolean_based_system_exit(
        ss_container.remove_owner(container_name, owner_name)
    )
