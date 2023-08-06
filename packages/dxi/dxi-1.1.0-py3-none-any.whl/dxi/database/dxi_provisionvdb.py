#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

"""
Provision Delphix Virtual Databases
"""
import time
from os.path import basename

from delphixpy.v1_10_2 import exceptions
from delphixpy.v1_10_2.web import database
from delphixpy.v1_10_2.web import environment
from delphixpy.v1_10_2.web import group
from delphixpy.v1_10_2.web import repository
from delphixpy.v1_10_2.web import sourceconfig
from delphixpy.v1_10_2.web import vo

from dxi._lib import dlpx_exceptions as dxe
from dxi._lib import dx_logging as log
from dxi._lib import get_references as ref
from dxi._lib import dx_timeflow as dxtf
from dxi._lib import run_job
from dxi._lib.dxi_constants import VirtualOps
from dxi._lib.run_async import run_async
from dxi.dxi_tool_base import DXIBase


class ProvisionVDBConstants(object):
    """
    Class of common constants used by Provision VDB
    """
    SINGLE_THREAD = False
    POLL = 10
    CONFIG = "config/dxtools.conf"
    LOG_FILE_PATH = "logs/dxi_provisionvdb.log"
    ENGINE_ID = "default"
    PARALLEL = 5
    ACTION = None
    MODULE_NAME = __name__
    VDB_LIST_HEADER = []
    FORCE = False


class DXIProvisionVDB(DXIBase):
    def __init__(
        self,
        engine=None,
        log_file_path=ProvisionVDBConstants.LOG_FILE_PATH,
        config=ProvisionVDBConstants.CONFIG,
        poll=ProvisionVDBConstants.POLL,
        single_thread=ProvisionVDBConstants.SINGLE_THREAD,
        parallel=ProvisionVDBConstants.PARALLEL,
        action=ProvisionVDBConstants.ACTION,
        module_name=ProvisionVDBConstants.MODULE_NAME,
        source_db=None,
        db=None,
        db_type=None,
        target_grp=None,
        env_name=None,
        mntpoint=None,
        timestamp=None,
        timestamp_type=None,
        prerefresh=None,
        postrefresh=None,
        prerollback=None,
        postrollback=None,
        configure_clone=None,
        envinst=None,
        version=False,
    ):
        super().__init__(
            parallel=parallel,
            poll=poll,
            config=config,
            log_file_path=log_file_path,
            single_thread=single_thread,
            module_name=module_name,
        )
        self.engine = engine
        self.source_db = source_db
        self.name = db
        self.group = target_grp
        self.db_type = db_type
        self.env_name = env_name
        self.mntpoint = mntpoint
        self.timestamp = timestamp
        self.timestamp_type = timestamp_type
        self.single_thread = single_thread
        self.pre_refresh = prerefresh
        self.post_refresh = postrefresh
        self.pre_rollback = prerollback
        self.post_rollback = postrollback
        self.configure_clone = configure_clone
        self.envinst = envinst
        self.parallel = parallel
        self.version = version
        self.time_start = time.time()
        self.dx_session_obj = self._initialize_session()
        self.poll = poll
        self.action = action

    def provision(self):
        # This is the function that will handle processing main_workflow for
        # all the servers.
        for each in run_job.run_job_mt(
                self.main_workflow, self.dx_session_obj, self.engine,
                self.single_thread
        ):
            each.join()

    def __provisionvdb_execution_helper(self):
        """
        Execution helper for Provision VDB
        :return:
        """
        try:
            self._execute_operation(self.main_workflow)
            return True
        except Exception:
            return False

    def _provision_ase_vdb(
        self,
        dlpx_obj,
        group_ref,
        vdb_name,
        source_obj,
        timestamp,
        timestamp_type="SNAPSHOT",
        no_truncate_log=False,
    ):
        """
        Create a Sybase ASE VDB
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param group_ref: Reference of Group name where the VDB will be created
        :type group_ref: str
        :param vdb_name: Name of the VDB
        :type vdb_name: str
        :param source_obj: Database object of the source
        :type source_obj: class
        delphixpy.v1_10_2.web.objects.UnixHostEnvironment.UnixHostEnvironment
        :param timestamp: The Delphix semantic for the point in time on the
            source from which to refresh the VDB
        :type timestamp: str
        :param timestamp_type: The Delphix semantic for the point in time on
        the source from which you want to refresh your VDB either
        SNAPSHOT or TIME
        :type timestamp_type: str
        :param no_truncate_log: Don't truncate log on checkpoint
        :type no_truncate_log: bool
        :return:
        """
        engine_name = list(dlpx_obj.dlpx_ddps)[0]
        dxtf_obj = dxtf.DxTimeflow(dlpx_obj.server_session)
        try:
            vdb_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, database, vdb_name
            )
            raise dxe.DlpxObjectExists(f"{vdb_obj} exists.")
        except dxe.DlpxObjectNotFound:
            pass
        vdb_params = vo.ASEProvisionParameters()
        vdb_params.container = vo.ASEDBContainer()
        if no_truncate_log:
            vdb_params.truncate_log_on_checkpoint = False
        else:
            vdb_params.truncate_log_on_checkpoint = True
        vdb_params.container.group = group_ref
        vdb_params.container.name = vdb_name
        vdb_params.source = vo.ASEVirtualSource()
        vdb_params.source.allow_auto_vdb_restart_on_host_reboot = True
        vdb_params.source_config = vo.ASESIConfig()
        vdb_params.source_config.database_name = vdb_name
        vdb_params.source_config.repository = ref.find_obj_by_name(
            dlpx_obj.server_session, repository, self.envinst
        ).reference
        vdb_params.timeflow_point_parameters = dxtf_obj.set_timeflow_point(
            source_obj, timestamp_type, timestamp
        )
        vdb_params.timeflow_point_parameters.container = source_obj.reference
        log.print_info(f"{engine_name} provisioning {vdb_name}")
        database.provision(dlpx_obj.server_session, vdb_params)
        # Add the job into the jobs dictionary so we can track its progress
        self._add_last_job_to_track(dlpx_obj)

    def _provision_mssql_vdb(
        self,
        dlpx_obj,
        vdb_name,
        group_ref,
        source_obj,
        timestamp,
        timestamp_type="SNAPSHOT"
    ):
        """
        Create a MSSQL VDB
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param group_ref: Reference of Group name where the VDB will be created
        :type group_ref: str
        :param vdb_name: Name of the VDB
        :type vdb_name: str
        :param source_obj: Database object of the source
        :type source_obj:
        :param timestamp: The Delphix semantic for the point in time on the
        source from which to refresh the VDB
        :type timestamp: str
        :param timestamp_type: The Delphix semantic for the point in time on
        the source from which you want to refresh your VDB either
        SNAPSHOT or TIME
        :type timestamp_type: str
        :return:
        """
        engine_name = list(dlpx_obj.dlpx_ddps)[0]
        timeflow_obj = dxtf.DxTimeflow(dlpx_obj.server_session)
        try:
            vdb_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, database, vdb_name
            )
            raise dxe.DlpxObjectExists(f"{vdb_obj} exists.")
        except dxe.DlpxObjectNotFound:
            pass
        vdb_params = vo.MSSqlProvisionParameters()
        vdb_params.container = vo.MSSqlDatabaseContainer()
        vdb_params.container.group = group_ref
        vdb_params.container.name = vdb_name
        vdb_params.source = vo.MSSqlVirtualSource()
        vdb_params.source.allow_auto_vdb_restart_on_host_reboot = False
        vdb_params.source_config = vo.MSSqlSIConfig()
        vdb_params.source_config.database_name = vdb_name
        vdb_params.source_config.repository = ref.find_obj_by_name(
            dlpx_obj.server_session, repository, self.envinst
        ).reference
        vdb_params.timeflow_point_parameters = timeflow_obj.set_timeflow_point(
            source_obj, timestamp_type, timestamp
        )
        vdb_params.timeflow_point_parameters.container = source_obj.reference
        log.print_info(f"{engine_name} provisioning {vdb_name}")
        database.provision(dlpx_obj.server_session, vdb_params)
        # Add the job into the jobs dictionary so we can track its progress
        self._add_last_job_to_track(dlpx_obj)

    def _provision_vfiles_vdb(
        self,
        dlpx_obj,
        group_ref,
        environment_obj,
        source_obj,
    ):
        """
        Create a vfiles VDB
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param group_ref: Reference of group name where the VDB will be created
        :type group_ref: str
        :param environment_obj: Environment object where the VDB will be created
        :type environment_obj: class 'delphixpy.v1_10_2.web.objects
        :param source_obj: vfiles object of the source
        :type source_obj: class
        delphixpy.v1_10_2.web.objects.OracleDatabaseContainer.OracleDatabaseContainer
        """
        engine_name = list(dlpx_obj.dlpx_ddps)[0]
        timeflow_obj = dxtf.DxTimeflow(dlpx_obj.server_session)
        try:
            vdb_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, database, self.name
            )
            raise dxe.DlpxObjectExists(f"{vdb_obj} exists.")
        except dxe.DlpxObjectNotFound:
            pass
        vfiles_params = vo.AppDataProvisionParameters()
        vfiles_params.source = vo.AppDataVirtualSource()
        vfiles_params.source_config = vo.AppDataDirectSourceConfig()
        vfiles_params.source.allow_auto_vdb_restart_on_host_reboot = True
        vfiles_params.container = vo.AppDataContainer()
        vfiles_params.container.group = group_ref
        vfiles_params.container.name = self.name
        vfiles_params.source_config.name = self.name
        vfiles_params.source_config.path = f"{self.mntpoint}/{self.name}"
        vfiles_params.source_config.repository = ref.find_db_repo(
            dlpx_obj.server_session,
            "AppDataRepository",
            environment_obj.reference,
            "Unstructured Files",
        )
        vfiles_params.source.name = self.name
        vfiles_params.source.parameters = {}
        vfiles_params.source.operations = vo.VirtualSourceOperations()
        if self.pre_refresh:
            vfiles_params.source.operations.pre_refresh = \
                vo.RunCommandOnSourceOperation()
            vfiles_params.source.operations.pre_refresh.command = \
                self.pre_refresh
        if self.post_refresh:
            vfiles_params.source.operations.post_refresh = \
                vo.RunCommandOnSourceOperation()
            vfiles_params.source.operations.post_refresh.command = \
                self.post_refresh
        if self.pre_rollback:
            vfiles_params.source.operations.pre_rollback = \
                vo.RunCommandOnSourceOperation
            vfiles_params.source.operations.pre_rollback.command = \
                self.pre_rollback
        if self.post_rollback:
            vfiles_params.source.operations.post_rollback = \
                vo.RunCommandOnSourceOperation()
            vfiles_params.source.operations.post_rollback.command = \
                self.post_rollback
        if self.configure_clone:
            vfiles_params.source.operations.configure_clone = (
                vo.RunCommandOnSourceOperation()
            )
            vfiles_params.source.operations.configure_clone.command = \
                self.configure_clone
        if self.timestamp_type is None:
            vfiles_params.timeflow_point_parameters = vo.TimeflowPointSemantic()
            vfiles_params.timeflow_point_parameters.container = \
                source_obj.reference
            vfiles_params.timeflow_point_parameters.location = "LATEST_POINT"
        elif self.timestamp_type.upper() == "SNAPSHOT":
            try:
                dx_snap_params = timeflow_obj.set_timeflow_point(
                    source_obj, self.timestamp_type, self.timestamp
                )
            except exceptions.RequestError as err:
                raise dxe.DlpxException(
                    f"Could not set the timeflow point:\n{err}"
                )
            if dx_snap_params.type == "TimeflowPointSemantic":
                vfiles_params.timeflow_point_parameters = \
                    vo.TimeflowPointSemantic()
                vfiles_params.timeflow_point_parameters.container = \
                    dx_snap_params.container
                vfiles_params.timeflow_point_parameters.location = \
                    dx_snap_params.location
            elif dx_snap_params.type == "TimeflowPointTimestamp":
                vfiles_params.timeflow_point_parameters = \
                    vo.TimeflowPointTimestamp()
                vfiles_params.timeflow_point_parameters.timeflow = \
                    dx_snap_params.timeflow
                vfiles_params.timeflow_point_parameters.timestamp = \
                    dx_snap_params.timestamp
        log.print_info(f"{engine_name}: Provisioning {self.name}\n")
        try:
            database.provision(dlpx_obj.server_session, vfiles_params)
        except (exceptions.RequestError, exceptions.HttpError) as err:
            raise dxe.DlpxException(
                f"ERROR: Could not provision the database {self.name}\n{err}"
            )
        # Add the job into the jobs dictionary so we can track its progress
        self._add_last_job_to_track(dlpx_obj)

    def _provision_oracle_si_vdb(
        self,
        dlpx_obj,
        group_ref,
        vdb_name,
        environment_obj,
        source_obj,
        mntpoint,
        timestamp,
        timestamp_type="SNAPSHOT"
    ):
        """
        Create an Oracle SI VDB
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param group_ref: Group name where the VDB will be created
        :type group_ref: str
        :param vdb_name: Name of the VDB
        :type vdb_name: str
        :param source_obj: Database object of the source
        :type source_obj: class
        delphixpy.v1_10_2.web.objects.OracleDatabaseContainer.OracleDatabaseContainer
        :param environment_obj: Environment object where the VDB will be created
        :type environment_obj: class 'delphixpy.v1_10_2.web.objects
        :param mntpoint: Where to mount the Delphix filesystem
        :type mntpoint: str
        :param timestamp: The Delphix semantic for the point in time on the
        source from which to refresh the VDB
        :type timestamp: str
        :param timestamp_type: The Delphix semantic for the point in time on
        the source from which you want to refresh your VDB either
        SNAPSHOT or TIME
        """
        engine_name = list(dlpx_obj.dlpx_ddps)[0]
        try:
            vdb_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, database, vdb_name
            )
            raise dxe.DlpxObjectExists(f"{vdb_obj} exists.")
        except dxe.DlpxObjectNotFound:
            pass
        vdb_params = vo.OracleProvisionParameters()
        vdb_params.open_resetlogs = True
        vdb_params.container = vo.OracleDatabaseContainer()
        vdb_params.container.group = group_ref
        vdb_params.container.name = vdb_name
        vdb_params.source = vo.OracleVirtualSource()
        vdb_params.source.allow_auto_vdb_restart_on_host_reboot = False
        vdb_params.source.mount_base = mntpoint
        vdb_params.source_config = vo.OracleSIConfig()
        vdb_params.source_config.environment_user = environment_obj.primary_user
        vdb_params.source.operations = vo.VirtualSourceOperations()
        if self.pre_refresh:
            vdb_params.source.operations.pre_refresh = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.pre_refresh.command = self.pre_refresh
        if self.post_refresh:
            vdb_params.source.operations.post_refresh = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.post_refresh.command = \
                self.post_refresh
        if self.pre_rollback:
            vdb_params.source.operations.pre_rollback = \
                vo.RunCommandOnSourceOperation
            vdb_params.source.operations.pre_rollback.command = \
                self.pre_rollback
        if self.post_rollback:
            vdb_params.source.operations.post_rollback = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.post_rollback.command = \
                self.post_rollback
        if self.configure_clone:
            vdb_params.source.operations.configure_clone = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.configure_clone.command = \
                self.configure_clone
        vdb_params.source_config.database_name = vdb_name
        vdb_params.source_config.unique_name = vdb_name
        vdb_params.source_config.instance = vo.OracleInstance()
        vdb_params.source_config.instance.instance_name = vdb_name
        vdb_params.source_config.instance.instance_number = 1
        vdb_params.source_config.repository = ref.find_db_repo(
            dlpx_obj.server_session, "OracleInstall",
            environment_obj.reference, self.envinst
        )
        timeflow_obj = dxtf.DxTimeflow(dlpx_obj.server_session)
        vdb_params.timeflow_point_parameters = timeflow_obj.set_timeflow_point(
            source_obj, timestamp_type, timestamp
        )
        log.print_info(f"{engine_name}: Provisioning {vdb_name}")
        try:
            database.provision(dlpx_obj.server_session, vdb_params)
        except (exceptions.RequestError, exceptions.HttpError) as err:
            raise dxe.DlpxException(
                f"ERROR: Could not provision the database {vdb_name}\n{err}"
            )
        # Add the job into the jobs dictionary so we can track its progress
        self._add_last_job_to_track(dlpx_obj)

    def _provision_oracle_mt_vdb(
            self, dlpx_obj, group_ref, vdb_name, source_obj, mntpoint,
            timestamp, timestamp_type='SNAPSHOT'
            ):
        """
        Create an Oracle Multi Tenant VDB
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param group_ref: Group name where the VDB will be created
        :type group_ref: str
        :param vdb_name: Name of the VDB
        :type vdb_name: str
        :param source_obj: Database object of the source
        :type source_obj: class
        delphixpy.v1_10_2.web.objects.OracleDatabaseContainer.OracleDatabaseContainer
        :param mntpoint: Where to mount the Delphix filesystem
        :type mntpoint: str
        :param timestamp: The Delphix semantic for the point in time on the
        source from which to refresh the VDB
        :type timestamp: str
        :param timestamp_type: The Delphix semantic for the point in time on
        the source from which you want to refresh your VDB either
        SNAPSHOT or TIME
        :type timestamp_type: str
        """
        engine_name = list(dlpx_obj.dlpx_ddps)[0]
        cdb_obj = ref.find_obj_by_name(
            dlpx_obj.server_session, sourceconfig, self.source_db)
        try:
            vdb_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, database, vdb_name)
            raise dxe.DlpxObjectExists(f'{vdb_obj} exists.')
        except dxe.DlpxObjectNotFound:
            pass
        vdb_params = vo.OracleMultitenantProvisionParameters()
        vdb_params.open_resetlogs = True
        vdb_params.container = vo.OracleDatabaseContainer()
        vdb_params.container.group = group_ref
        vdb_params.container.name = vdb_name
        vdb_params.source = vo.OracleVirtualPdbSource()
        vdb_params.source.allow_auto_vdb_restart_on_host_reboot = True
        vdb_params.source.mount_base = mntpoint
        vdb_params.source_config = vo.OraclePDBConfig()
        vdb_params.source_config.database_name = vdb_name
        vdb_params.source_config.cdb_config = cdb_obj.cdb_config
        vdb_params.source.operations = vo.VirtualSourceOperations()
        if self.pre_refresh:
            vdb_params.source.operations.pre_refresh = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.pre_refresh.command = self.pre_refresh
        if self.post_refresh:
            vdb_params.source.operations.post_refresh = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.post_refresh.command = \
                self.post_refresh
        if self.pre_rollback:
            vdb_params.source.operations.pre_rollback = \
                vo.RunCommandOnSourceOperation
            vdb_params.source.operations.pre_rollback.command = \
                self.pre_rollback
        if self.post_rollback:
            vdb_params.source.operations.post_rollback = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.post_rollback.command = \
                self.post_rollback
        if self.configure_clone:
            vdb_params.source.operations.configure_clone = \
                vo.RunCommandOnSourceOperation()
            vdb_params.source.operations.configure_clone.command = \
                self.configure_clone
        timeflow_obj = dxtf.DxTimeflow(dlpx_obj.server_session)
        vdb_params.timeflow_point_parameters = \
            timeflow_obj.set_timeflow_point(source_obj, timestamp_type,
                                            timestamp)
        log.print_info(f'{engine_name}: Provisioning {vdb_name}')
        try:
            database.provision(dlpx_obj.server_session, vdb_params)
        except (exceptions.RequestError, exceptions.HttpError) as err:
            raise dxe.DlpxException(
                f'ERROR: Could not provision the database {vdb_name}\n{err}')
        # Add the job into the jobs dictionary so we can track its progress
        self._add_last_job_to_track(dlpx_obj)

    def _provision_vdb_helper(self, dlpx_obj):
        group_ref = None
        environment_obj = None
        source_obj = None
        if self.group:
            group_ref = ref.find_obj_by_name(
                dlpx_obj.server_session, group, self.group
            ).reference
        if self.env_name:
            environment_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, environment, self.env_name
            )
        if self.source_db:
            source_obj = ref.find_obj_by_name(
                dlpx_obj.server_session, database, self.source_db
            )
        if self.db_type.lower() == "oracle":
            self._provision_oracle_si_vdb(
                dlpx_obj, group_ref, self.name, environment_obj, source_obj,
                self.mntpoint, self.timestamp, self.timestamp_type
            )
        elif self.db_type.lower() == "oramt":
            self._provision_oracle_mt_vdb(
                dlpx_obj, group_ref, self.name, source_obj, self.mntpoint,
                self.timestamp, self.timestamp_type
            )
        elif self.db_type.lower() == "mssql":
            self._provision_mssql_vdb(
                dlpx_obj, self.name, group_ref, source_obj,
                self.timestamp, self.timestamp_type
            )
        elif self.db_type.lower() == "vfiles":
            self._provision_vfiles_vdb(
                dlpx_obj, group_ref, environment_obj, source_obj
            )
        elif self.db_type.lower() == "ase":
            self._provision_ase_vdb(
                dlpx_obj, group_ref, self.name, source_obj,
                self.timestamp, self.timestamp_type
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
                    self._provision_vdb_helper(dlpx_obj)
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
