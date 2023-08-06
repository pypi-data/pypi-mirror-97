#
# Copyright (c) 2021 by Delphix. All rights reserved.
#
"""
Create and sync a dSource
"""

import time
from os.path import basename

from delphixpy.v1_10_2 import exceptions
from dxi._lib import dlpx_exceptions as dxe
from dxi._lib import dx_logging as log
from dxi._lib import run_job
from dxi._lib import dsource_link_ase
from dxi._lib import dsource_link_mssql
from dxi._lib import dsource_link_oracle
from dxi._lib.dxi_constants import VirtualOps
from dxi._lib.run_async import run_async
from dxi.dxi_tool_base import DXIBase


class ProvisionDsourceConstants(object):
    """
    Class of common constants used by Provision dSource
    """
    SINGLE_THREAD = False
    POLL = 10
    CONFIG = "config/dxtools.conf"
    LOG_FILE_PATH = "logs/dxi_provisiondsource.log"
    ENGINE_ID = "default"
    PARALLEL = 5
    ACTION = None
    MODULE_NAME = __name__
    VDB_LIST_HEADER = []
    FORCE = False


class DXIProvisionDsource(DXIBase):
    def __init__(
        self,
        engine=None,
        log_file_path=ProvisionDsourceConstants.LOG_FILE_PATH,
        config=ProvisionDsourceConstants.CONFIG,
        poll=ProvisionDsourceConstants.POLL,
        single_thread=ProvisionDsourceConstants.SINGLE_THREAD,
        parallel=ProvisionDsourceConstants.PARALLEL,
        action=ProvisionDsourceConstants.ACTION,
        module_name=ProvisionDsourceConstants.MODULE_NAME,
        ip_addr=None,
        env_name=None,
        dx_group=None,
        dsource_name=None,
        db_user=None,
        db_passwd=None,
        db_install_path=None,
        num_connections=None,
        logsync=None,
        envinst=None,
        files_per_set=None,
        rman_channels=None,
        create_bckup=None,
        bck_file=None,
        port_num=None,
        ase_passwd=None,
        ase_user=None,
        backup_path=None,
        sync_mode=None,
        source_user=None,
        stage_user=None,
        logsync_mode=None,
        stage_repo=None,
        stage_instance=None,
        stage_env=None,
        db_type=None,
        initial_load_type=None,
        delphix_managed=True,
        validated_sync_mode=None,
        backup_loc_passwd=None,
        backup_loc_user=None,
        load_from_backup=None,
        version=False
    ):
        super().__init__(
            parallel=parallel,
            poll=poll,
            config=config,
            log_file_path=log_file_path,
            single_thread=single_thread,
            module_name=module_name,
        )
        self.dsource_name = dsource_name
        self.db_passwd = db_passwd
        self.db_user = db_user
        self.dx_group = dx_group
        self.env_name = env_name
        self.envinst = envinst
        self.ip_addr = ip_addr
        self.db_type = db_type
        self.logsync_mode = logsync_mode
        self.port_num = port_num
        self.engine = engine
        self.num_connections = num_connections
        self.files_per_set = files_per_set
        self.rman_channels = rman_channels
        self.create_bckup = create_bckup
        self.bck_file = bck_file
        self.db_install_path = db_install_path
        self.backup_loc_passwd = backup_loc_passwd
        self.backup_loc_user = backup_loc_user
        self.load_from_backup = load_from_backup
        self.ase_passwd = ase_passwd
        self.ase_user = ase_user
        self.backup_path = backup_path
        self.sync_mode = sync_mode
        self.source_user = source_user
        self.stage_user = stage_user
        self.stage_repo = stage_repo
        self.stage_instance = stage_instance
        self.validated_sync_mode = validated_sync_mode
        self.single_thread = single_thread
        self.logsync = logsync
        self.stage_env=stage_env
        self.parallel = parallel
        self.poll = poll
        self.initial_load_type = initial_load_type
        self.delphix_managed = delphix_managed
        self.config = config
        self.version = version
        self.time_start = time.time()
        self.dx_session_obj = self._initialize_session()
        self.action = action

    def execute(self):
        # This is the function that will handle processing main_workflow for
        # all the servers.
        for each in run_job.run_job_mt(
                self.main_workflow, self.dx_session_obj, self.engine,
                self.single_thread
        ):
            each.join()
        elapsed_minutes = run_job.time_elapsed(self.time_start)
        log.print_info(
            f"script took {elapsed_minutes} minutes to get this far."
        )

    def _provision_dsource_helper(self, dlpx_obj):
        if self.db_type.lower() == "oracle":
            linked_ora = dsource_link_oracle.DsourceLinkOracle(
                dlpx_obj,
                self.dsource_name,
                self.db_passwd,
                self.db_user,
                self.dx_group,
                self.logsync,
                self.logsync_mode,
                self.db_type
            )
            linked_ora.get_or_create_ora_sourcecfg(
                self.env_name,
                self.db_install_path,
                self.ip_addr,
                self.port_num,
            )
        elif self.db_type.lower() == "sybase":
            ase_obj = dsource_link_ase.DsourceLinkASE(
                dlpx_obj,
                self.dsource_name,
                self.db_passwd,
                self.db_user,
                self.dx_group,
                self.logsync,
                self.stage_repo,
                self.db_type
            )
            ase_obj.link_ase_dsource(
                self.backup_path,
                self.bck_file,
                self.create_bckup,
                self.env_name
            )
        elif self.db_type.lower() == "mssql":
            mssql_obj = dsource_link_mssql.DsourceLinkMssql(
                dlpx_obj,
                self.dsource_name,
                self.db_passwd,
                self.db_user,
                self.dx_group,
                self.db_type,
                self.logsync,
                self.validated_sync_mode,
                self.initial_load_type,
                self.delphix_managed
            )
            mssql_obj.link_mssql_dsource(
                self.stage_env,
                self.stage_instance,
                self.backup_path,
                self.backup_loc_passwd,
                self.backup_loc_user,
                uuid='Any'
            )

    @run_async
    def main_workflow(self, engine, dlpx_obj, single_thread):
        """
        This function is where we create our main workflow.
        Use the @run_async decorator to run this function asynchronously.
        The @run_async decorator to run multithreaded on Delphix Engines
        simultaneously
        :param engine: Dictionary of engines
        :type engine: dictionary
        :param single_thread: True - run single threaded,
                               False - run multi-thread
        :type single_thread: bool
        """
        err = None
        dlpx_obj = self._initialize_session()
        self._setup_dlpx_session(dlpx_obj, engine)
        if dlpx_obj.server_session:
            try:
                with dlpx_obj.job_mode(single_thread):
                    self._provision_dsource_helper(dlpx_obj)
                    run_job.track_running_jobs(engine, dlpx_obj, self.poll)
            except (
                dxe.DlpxException,
                exceptions.RequestError,
                exceptions.JobError,
                exceptions.HttpError,
            ) as err:
                log.print_exception(
                    f"Error in {basename(__file__)}:"
                    f'{engine["hostname"]}\n ERROR: {err}'
                )
            raise err
