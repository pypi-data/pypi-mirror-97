#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib import click_util
from dxi._lib.util import boolean_based_system_exit
from dxi.snapshot.dxi_snapshot import DXISnapshot
from dxi.snapshot.dxi_snapshot import SnapshotConstants


@click.group()
def snapshot():
    """
    To Add and Delete snapshots
    """
    pass


@snapshot.command()
@click.option(
    "--group",
    cls=click_util.MutuallyExclusiveOption,
    mutually_exclusive=["name", "all_dbs"],
    default=SnapshotConstants.GROUP,
    help="Name of group in Delphix to refresh against",
)
@click.option(
    "--name",
    cls=click_util.MutuallyExclusiveOption,
    default=SnapshotConstants.NAME,
    mutually_exclusive=["group", "all_dbs"],
    help="Name of object in Delphix to refresh against",
)
@click.option(
    "--all_dbs",
    cls=click_util.MutuallyExclusiveOption,
    mutually_exclusive=["name", "group"],
    is_flag=True,
    default=SnapshotConstants.ALL_DBS,
    help="Run against all database objects",
)
@click.option("--engine", default=SnapshotConstants.ENGINE_ID)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=SnapshotConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=SnapshotConstants.PARALLEL,
)
@click.option(
    "--poll",
    help="The number of seconds to wait between job polls.",
    default=SnapshotConstants.POLL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=SnapshotConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=SnapshotConstants.LOG_FILE_PATH,
)
@click.option(
    "--bck_file",
    help="Name of the specific ASE Sybase backup "
    "file(s) or backup uuid for MSSQL",
    default=SnapshotConstants.BCK_FILE,
)
@click.option(
    "--usebackup",
    help='Snapshot using "Most Recent backup '
    "Available for MSSQL and ASE only.",
    default=SnapshotConstants.USE_BACKUP,
    is_flag=True,
)
@click.option(
    "--create_bckup",
    help=" Create and ingest a new Sybase"
    " backup or copy-only MS SQL backup.",
    default=SnapshotConstants.CREATE_BACKUP,
    is_flag=True,
)
def create(
    group,
    name,
    all_dbs,
    engine,
    single_thread,
    bck_file,
    usebackup,
    create_bckup,
    parallel,
    poll,
    config,
    log_file_path,
):
    """

Snapshot a Delphix dSource or VDB

dxi snapshot create --group UAT

    """
    snapshot_obj = DXISnapshot(
        engine=engine,
        group=group,
        name=name,
        all_dbs=all_dbs,
        parallel=parallel,
        poll=poll,
        config=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(snapshot_obj.create_snapshot(
        usebackup=usebackup, create_bckup=create_bckup, bck_file=bck_file
    ))


if __name__ == "__main__":
    create()
