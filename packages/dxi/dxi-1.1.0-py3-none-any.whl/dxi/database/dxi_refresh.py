#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

from delphixpy.v1_10_2 import exceptions
from delphixpy.v1_10_2.web import database
from delphixpy.v1_10_2.web import vo
from dxi._lib import dlpx_exceptions
from dxi._lib import dx_logging
from dxi._lib import dx_timeflow
from dxi._lib import get_references
from dxi._lib import run_job
from dxi._lib.run_async import run_async
from dxi.dxi_tool_base import DXIBase


class VDBRefreshConstants(object):
    """
    Define constants for VDBRefresh class and CLI usage
    """

    SINGLE_THREAD = False
    POLL = 20
    CONFIG = "config/dxtools.conf"
    LOG_FILE_PATH = "logs/dxi_refresh.log"
    ENGINE_ID = "default"
    TIME_STAMP_TYPE = ("SNAPSHOT",)
    TIME_STAMP = "LATEST"
    TIME_FLOW = None
    PARALLEL = 5


class DXIRefresh(DXIBase):
    """
    Refresh a Delphix VDB
    """

    def __init__(
        self,
        name,
        time_stamp_type=VDBRefreshConstants.TIME_STAMP_TYPE,
        time_stamp=VDBRefreshConstants.TIME_STAMP,
        time_flow=VDBRefreshConstants.TIME_FLOW,
        engine=VDBRefreshConstants.ENGINE_ID,
        single_thread=VDBRefreshConstants.SINGLE_THREAD,
        poll=VDBRefreshConstants.POLL,
        config=VDBRefreshConstants.CONFIG,
        log_file_path=VDBRefreshConstants.LOG_FILE_PATH,
        parallel=VDBRefreshConstants.PARALLEL,
    ):
        """
          :param name: VDBs name
          :type name: `str`
          :param time_stamp_type: Either SNAPSHOT or TIME
          :type time_stamp_type: `str`
          :param time_stamp: The Delphix semantic for the point in time on
                the source from which you want to refresh your VDB.
          :type time_stamp: `str`
          :param time_flow: Name of the timeflow to refresh a VDB
          :type time_flow: `str`
          :param engine: An Identifier of Delphix engine in dxtools.conf.
          :type engine: `str`
          :param single_thread: Run as a single thread.
                 False if running multiple threads.
          :type single_thread: `bool`
          :param poll: The number of seconds to wait between job polls
          :type poll: `int`
          :param config: The path to the dxtools.conf file
          :type config: `str`
          :param log_file_path: The path to the logfile you want to use.
          :type log_file_path: `str`
          :param all_dbs: Run against all database objects
          :type all_dbs: `bool`
        """
        super().__init__(
            poll=poll,
            config=config,
            log_file_path=log_file_path,
            single_thread=single_thread,
            engine=engine,
            module_name=__name__,
            parallel=parallel,
        )
        self.vdb = name
        self.time_stamp_type = time_stamp_type
        self.time_stamp = time_stamp
        self.time_flow = time_flow
        self.display_choices(self)

    def refresh(self):
        """
        Refresh a Delphix VDB
        """
        try:
            self._execute_operation(self._refresh_helper)
            return True
        except (Exception, BaseException):
            return False

    def _run_refresh_for_vdb(self, dlpx_obj):
        """
        :param dlpx_obj: DDP session object
        :type dlpx_obj: `lib.GetSession.GetSession`
        """
        for vdb_name in self.vdb.split(":"):
            dx_timeflow_obj = dx_timeflow.DxTimeflow(dlpx_obj.server_session)
            dx_logging.print_debug(f" Refreshing {vdb_name}")
            container_obj = get_references.find_obj_by_name(
                dlpx_obj.server_session, database, vdb_name
            )
            source_obj = get_references.find_source_by_db_name(
                dlpx_obj.server_session, vdb_name
            )
            # Sanity check to make sure our container object has a reference
            if container_obj.reference:
                try:
                    if (
                        source_obj.virtual is not True
                        or source_obj.staging is True
                    ):
                        dx_logging.print_exception(
                            f"{self.vdb} is not a virtual object.\n"
                        )
                    elif source_obj.runtime.enabled == "ENABLED":
                        dx_logging.print_debug(
                            f"INFO: Refreshing {self.vdb} "
                            f"to {self.time_stamp}\n"
                        )
                # This exception is raised if refreshing a vFiles VDB since
                # AppDataContainer does not have virtual,
                # staging or enabled attributes
                except AttributeError:
                    pass
            if source_obj.reference:
                try:
                    source_db = database.get(
                        dlpx_obj.server_session,
                        container_obj.provision_container,
                    )
                except (exceptions.RequestError, exceptions.JobError) as err:
                    raise dlpx_exceptions.DlpxException(
                        f"Encountered error while refreshing:"
                        f"{vdb_name}:\n{err}"
                    )

                if str(container_obj.reference).startswith("ORACLE"):
                    refresh_params = vo.OracleRefreshParameters()
                else:
                    refresh_params = vo.RefreshParameters()

                refresh_params.timeflow_point_parameters = dx_timeflow_obj.set_timeflow_point(  # noqa
                    source_db, self.time_stamp_type, self.time_stamp
                )
                try:
                    database.refresh(
                        dlpx_obj.server_session,
                        container_obj.reference,
                        refresh_params,
                    )
                    self._add_last_job_to_track(dlpx_obj)
                except (
                    dlpx_exceptions.DlpxException,
                    exceptions.RequestError,
                ) as err:
                    dx_logging.print_exception(
                        f"ERROR: Could not set timeflow point:{err}"
                    )
                    raise dlpx_exceptions.DlpxException(
                        f"ERROR: Could not set time flow point:{err}"
                    )
            # Don't do anything if the database is disabled
            else:
                dx_logging.print_debug(
                    f"INFO: {container_obj.name} is not enabled."
                    f" Refresh will not continue.\n"
                )

    @run_async
    def _refresh_helper(self, engine, dlpx_obj, single_thread):
        """
        This function is where we create our main workflow.
        Use the @run_async decorator to run this function asynchronously.
        The @run_async decorator allows us to run against multiple
        Delphix Engine simultaneously
        :param engine: Dictionary of engines
        :type engine: `dict`
        :param dlpx_obj: DDP session object
        :type dlpx_obj: `lib.GetSession.GetSession`
        :param single_thread: True - run single threaded, False -
            run multi-thread
        :type single_thread: `bool`
        """
        dlpx_obj = self._initialize_session()
        self._setup_dlpx_session(dlpx_obj, engine)
        try:
            with dlpx_obj.job_mode(single_thread):
                self._run_refresh_for_vdb(dlpx_obj)
                dx_logging.print_debug(f"All refreshes must be running now")
                run_job.track_running_jobs(
                    engine, dlpx_obj, poll=self.poll, failures=self.failures
                )
        except (Exception, BaseException) as err:
            dx_logging.print_exception(
                f"Error in dx_refresh_vdb:" f'{engine["ip_address"]}\n{err}'
            )
            self.failures[0] = True
