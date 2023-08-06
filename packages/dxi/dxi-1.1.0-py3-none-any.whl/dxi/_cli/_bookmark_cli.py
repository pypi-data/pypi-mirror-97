#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import click
from dxi._lib import click_util
from dxi._lib.util import boolean_based_system_exit
from dxi.bookmark.dxi_bookmark import BookmarkConstants
from dxi.bookmark.dxi_bookmark import DXIBookmark


@click.group()
def bookmark():
    """
    Group command for Bookmark operations
    """
    pass


# list
@bookmark.command()
@click.option("--tags", default=None, help="Tags to filter the bookmark names")
@click.option(
    "--engine",
    default=BookmarkConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=BookmarkConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=BookmarkConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=BookmarkConstants.PARALLEL,
)
@click.option(
    "--configfile",
    help="The path to the dxtools.conf file.",
    default=BookmarkConstants.CONFIG,
)
@click.option(
    "--logfile",
    help="The path to the logfile you want to use.",
    default=BookmarkConstants.LOG_FILE_PATH,
)
def list(engine, single_thread, parallel, poll, configfile, logfile, tags):
    """
    List all Bookmarks on an engine
    """
    bmk_obj = DXIBookmark(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=configfile,
        log_file_path=logfile,
        single_thread=single_thread,
    )
    boolean_based_system_exit(bmk_obj.list(tags=tags))


# share
@bookmark.command()
@click.option(
    "--bookmarkname",
    default=None,
    required=True,
    help="Name of the bookmark to share",
)
@click.option(
    "--engine",
    default=BookmarkConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=BookmarkConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=BookmarkConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=BookmarkConstants.PARALLEL,
)
@click.option(
    "--configfile",
    help="The path to the dxtools.conf file.",
    default=BookmarkConstants.CONFIG,
)
@click.option(
    "--logfile",
    help="The path to the logfile you want to use.",
    default=BookmarkConstants.LOG_FILE_PATH,
)
def share(
    bookmarkname, engine, single_thread, parallel, poll, configfile, logfile
):
    """
    Share a bookmark by name
    """
    bmk_obj = DXIBookmark(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=configfile,
        log_file_path=logfile,
        single_thread=single_thread,
    )
    boolean_based_system_exit(bmk_obj.share(bookmark_name=bookmarkname))


# unshare
@bookmark.command()
@click.option(
    "--bookmarkname",
    default=None,
    required=True,
    help="Name of the bookmark to unshare",
)
@click.option(
    "--engine",
    default=BookmarkConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=BookmarkConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=BookmarkConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=BookmarkConstants.PARALLEL,
)
@click.option(
    "--configfile",
    help="The path to the dxtools.conf file.",
    default=BookmarkConstants.CONFIG,
)
@click.option(
    "--logfile",
    help="The path to the logfile you want to use.",
    default=BookmarkConstants.LOG_FILE_PATH,
)
def unshare(
    bookmarkname, engine, single_thread, parallel, poll, configfile, logfile
):
    """
    Unshare a bookmark using bookmark name
    """
    bmk_obj = DXIBookmark(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=configfile,
        log_file_path=logfile,
        single_thread=single_thread,
    )
    boolean_based_system_exit(bmk_obj.unshare(bookmark_name=bookmarkname))


# delete
@bookmark.command()
@click.option(
    "--bookmarkname",
    default=None,
    required=True,
    help="Name of the bookmark to delete",
)
@click.option(
    "--engine",
    default=BookmarkConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=BookmarkConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=BookmarkConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=BookmarkConstants.PARALLEL,
)
@click.option(
    "--configfile",
    help="The path to the dxtools.conf file.",
    default=BookmarkConstants.CONFIG,
)
@click.option(
    "--logfile",
    help="The path to the logfile you want to use.",
    default=BookmarkConstants.LOG_FILE_PATH,
)
def delete(
    bookmarkname, engine, single_thread, parallel, poll, configfile, logfile
):
    """
    Delete a bookmark using bookmark name
    """
    bmk_obj = DXIBookmark(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=configfile,
        log_file_path=logfile,
        single_thread=single_thread,
    )
    boolean_based_system_exit(bmk_obj.delete(bookmark_name=bookmarkname))


# update
@bookmark.command()
@click.option(
    "--bookmarkname",
    default=None,
    required=True,
    help="Name of the bookmark to update",
)
@click.option(
    "--newname",
    default=None,
    help="If updating bookmark name, provide new name",
)
@click.option(
    "--tags",
    default=None,
    help="If updating tags, provide new tags. "
    "All existing tags on the bookmark will be replaced with new tags",
)
@click.option(
    "--description",
    default=None,
    help="If updating description, provide new description",
)
@click.option(
    "--expires",
    default=None,
    help="If updating expiration, provide new expiration date-time"
    'Format: "%Y-%m-%dT%H:%M:%S" ',
)
@click.option(
    "--engine",
    default=BookmarkConstants.ENGINE_ID,
    help="Name of the engine to run this operation on",
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=BookmarkConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=BookmarkConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=BookmarkConstants.PARALLEL,
)
@click.option(
    "--configfile",
    help="The path to the dxtools.conf file.",
    default=BookmarkConstants.CONFIG,
)
@click.option(
    "--logfile",
    help="The path to the logfile you want to use.",
    default=BookmarkConstants.LOG_FILE_PATH,
)
def update(
    bookmarkname,
    newname,
    tags,
    description,
    expires,
    engine,
    single_thread,
    parallel,
    poll,
    configfile,
    logfile,
):
    """
    Updates a bookmark using a bookmark name
    """
    bmk_obj = DXIBookmark(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=configfile,
        log_file_path=logfile,
        single_thread=single_thread,
    )
    boolean_based_system_exit(
        bmk_obj.update(
            bookmark_name=bookmarkname,
            new_bookmark_name=newname,
            tags=tags,
            description=description,
            expires=expires,
        )
    )


# create
@bookmark.command()
@click.option(
    "--bookmarkname",
    default=None,
    required=True,
    help="Name of the bookmark to create",
)
@click.option(
    "--containername",
    cls=click_util.MutuallyExclusiveOption,
    mutually_exclusive=["templatename"],
    default=None,
    help="\b\nName of the container to create the bookmark\n"
    "[required] if bookmark is being created on a container",
)
@click.option(
    "--templatename",
    cls=click_util.MutuallyExclusiveOption,
    mutually_exclusive=["containername"],
    default=None,
    help="\b\nName of the template to create the bookmark.\n"
    "[required] if bookmark is being created on a template",
)
@click.option(
    "--branchname",
    default=None,
    help="\b\nIf bookmark is not unique in a container,\n "
    "specify the branch to create the bookmark from",
)
@click.option(
    "--timestamp",
    default=None,
    help="Timestamp to create the bookmark. "
    'Format: "%Y-%m-%dT%H:%M:%S" | latest',
)
@click.option(
    "--expires",
    default=None,
    help='Set bookmark expiration time. Format "%Y-%m-%dT%H:%M:%S"',
)
@click.option("--tags", default=None, help="Tags to set on the bookmark")
@click.option(
    "--description", default=None, help="Description for the bookmark"
)
@click.option(
    "--engine", help="Name of the engine", default=BookmarkConstants.ENGINE_ID
)
@click.option(
    "--single_thread",
    help="Run as a single thread",
    default=BookmarkConstants.SINGLE_THREAD,
    is_flag=True,
)
@click.option(
    "--poll",
    type=click.INT,
    help="The number of seconds to wait between job polls.",
    default=BookmarkConstants.POLL,
)
@click.option(
    "--parallel",
    type=click.INT,
    help="Limit number of jobs to maxjob.",
    default=BookmarkConstants.PARALLEL,
)
@click.option(
    "--config",
    help="The path to the dxtools.conf file.",
    default=BookmarkConstants.CONFIG,
)
@click.option(
    "--log_file_path",
    help="The path to the logfile you want to use.",
    default=BookmarkConstants.LOG_FILE_PATH,
)
def create(
    bookmarkname,
    containername,
    templatename,
    branchname,
    timestamp,
    expires,
    tags,
    description,
    engine,
    single_thread,
    parallel,
    poll,
    config,
    log_file_path,
):
    """
    Create a new bookmark
    """
    bmk_obj = DXIBookmark(
        engine=engine,
        parallel=parallel,
        poll=poll,
        config_file=config,
        log_file_path=log_file_path,
        single_thread=single_thread,
    )
    boolean_based_system_exit(
        bmk_obj.create(
            bookmark_name=bookmarkname,
            container_name=containername,
            template_name=templatename,
            branch_name=branchname,
            timestamp=timestamp,
            expires=expires,
            tags=tags,
            description=description,
        )
    )


if __name__ == "__main__":
    list()
