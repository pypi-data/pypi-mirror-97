#
# Copyright (c) 2021 by Delphix. All rights reserved.
#
"""
List all VDBs, start, stop, enable, disable a VDB
"""
from os.path import basename

from delphixpy.v1_10_2 import exceptions
from delphixpy.v1_10_2.web import source
from delphixpy.v1_10_2.web.capacity import consumer
from delphixpy.v1_10_2.web.vo import SourceDisableParameters
from dxi._lib import dlpx_exceptions as dxe
from dxi._lib import dx_logging as log
from dxi._lib import get_references as ref
from dxi._lib import run_job
from dxi._lib.dxi_constants import VirtualOps
from dxi._lib.run_async import run_async
from dxi.dxi_tool_base import DXIBase


class DXIDBOperationsConstants(object):
    """
    Class of common constants used by DB Operations
    """

    SINGLE_THREAD = False
    POLL = 20
    CONFIG = "config/dxtools.conf"
    LOG_FILE_PATH = "logs/dxi_dboperations.log"
    ENGINE_ID = "default"
    PARALLEL = 5
    ACTION = None
    MODULE_NAME = __name__
    VDB_LIST_HEADER = []
    FORCE = False


class DXIDBOperations(DXIBase):
    """
    Delphix Integration class for comman DB Operations

    This class contains all methods to perform the following \
    operations on datasets
    Virtual Operations: Start | Stop | Enable | Disable
    Source Operations: Link | Unlink
    """

    def __init__(
        self,
        engine=DXIDBOperationsConstants.ENGINE_ID,
        log_file_path=DXIDBOperationsConstants.LOG_FILE_PATH,
        config_file=DXIDBOperationsConstants.CONFIG,
        poll=DXIDBOperationsConstants.POLL,
        single_thread=DXIDBOperationsConstants.SINGLE_THREAD,
        parallel=DXIDBOperationsConstants.PARALLEL,
        action=DXIDBOperationsConstants.ACTION,
        module_name=DXIDBOperationsConstants.MODULE_NAME,
    ):
        super().__init__(
            parallel=parallel,
            poll=poll,
            config=config_file,
            log_file_path=log_file_path,
            single_thread=single_thread,
            module_name=module_name,
        )
        self.action = action
        self.engine = engine
        self.name = ""
        self.group = ""
        self.force = DXIDBOperationsConstants.FORCE

    def list(self):
        """
        List datasets on an engine
        """
        self.action = VirtualOps.LIST
        try:
            self.__dboperations_execution_helper()
            log.print_debug(">>> End Execution <<<")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"listing the datasets: {repr(err)}"
            )
            return False

    def start(self, name, group=None):
        """
        Start a Virtual dataset by name
        """
        self.action = VirtualOps.START
        self.name = name
        self.group = group
        try:
            self.__dboperations_execution_helper()
            log.print_debug(">>> End Execution <<<")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"starting the virtual dataset: {repr(err)}"
            )
            return False

    def stop(self, name, group=None):
        """
        Stop a Virtual dataset by name
        """
        self.action = VirtualOps.STOP
        self.name = name
        self.group = group
        try:
            self.__dboperations_execution_helper()
            log.print_debug(">>> End Execution <<<")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"stoping the virtual dataset: {repr(err)}"
            )
            return False

    def enable(self, name, group=None):
        """
        Enable a Virtual dataset by name
        """
        self.action = VirtualOps.ENABLE
        self.name = name
        self.group = group
        try:
            self.__dboperations_execution_helper()
            log.print_debug(">>> End Execution <<<")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"enabling the virtual dataset: {repr(err)}"
            )
            return False

    def disable(self, name, group=None, force=DXIDBOperationsConstants.FORCE):
        """
        Disable a Virtual dataset by name
        """
        self.action = VirtualOps.DISABLE
        self.name = name
        self.group = group
        self.force = force
        try:
            self.__dboperations_execution_helper()
            log.print_debug(">>> End Execution <<<")
            return True
        except Exception as err:
            log.print_exception(
                f"An Error was encountered while "
                f"disabling the virtual dataset: {repr(err)}"
            )
            return False

    def __dboperations_execution_helper(self):
        """
        Execution helper for DB Operations
        :return:
        """
        try:
            self._execute_operation(self.main_workflow)
            return True
        except Exception:
            return False

    def _start(self, dlpx_obj):
        """
        Starts a dataset
        :return:
        """
        svr_session = dlpx_obj.server_session
        try:
            if self.group:
                vdb_container_obj = ref.find_db_by_name_and_group(
                    svr_session, self.group, self.name, False
                )
                vdb_obj = ref.find_source_obj_by_containerref(
                    svr_session, source, vdb_container_obj.reference
                )
            else:
                vdb_obj = ref.find_obj_by_name(svr_session, source, self.name)
            source.start(svr_session, vdb_obj.reference)
            self._add_last_job_to_track(dlpx_obj)
        except (
            exceptions.RequestError,
            exceptions.JobError,
            AttributeError,
        ) as err:
            log.print_exception(
                f"An error occurred while starting dataset {self.name}: {err}"
            )
            # raise dxe.DlpxException(
            #     f"An error occurred while starting dataset {self.name}:
            #     {err}"
            # )
            self.failures[0] = True

    def _stop(self, dlpx_obj):
        """
        Stops a dataset
        :return:
        """
        svr_session = dlpx_obj.server_session
        try:
            if self.group:
                vdb_container_obj = ref.find_db_by_name_and_group(
                    svr_session, self.group, self.name, False
                )
                vdb_obj = ref.find_source_obj_by_containerref(
                    svr_session, source, vdb_container_obj.reference
                )
            else:
                vdb_obj = ref.find_obj_by_name(svr_session, source, self.name)
            source.stop(svr_session, vdb_obj.reference)
            self._add_last_job_to_track(dlpx_obj)
        except (
            exceptions.RequestError,
            exceptions.JobError,
            AttributeError,
        ) as err:
            log.print_exception(
                f"An error occurred while stopping dataset {self.name}: {err}"
            )
            # raise dxe.DlpxException(
            #     f"An error occurred while stopping dataset {self.name}:
            #     {err}"
            # )
            self.failures[0] = True

    def _enable(self, dlpx_obj):
        """
        Enables a dataset
        :return:
        """
        svr_session = dlpx_obj.server_session
        try:
            if self.group:
                vdb_container_obj = ref.find_db_by_name_and_group(
                    svr_session, self.group, self.name, False
                )
                vdb_obj = ref.find_source_obj_by_containerref(
                    svr_session, source, vdb_container_obj.reference
                )
            else:
                vdb_obj = ref.find_obj_by_name(svr_session, source, self.name)
            source.enable(svr_session, vdb_obj.reference)
            self._add_last_job_to_track(dlpx_obj)
        except (
            exceptions.RequestError,
            exceptions.JobError,
            AttributeError,
        ) as err:
            log.print_exception(
                f"An error occurred while enabling dataset {self.name}: {err}"
            )
            # raise dxe.DlpxException(
            #     f"An error occurred while enabling dataset {self.name}:
            #     {err}"
            # )
            self.failures[0] = True

    def _disable(self, dlpx_obj):
        """
        Disables a dataset
        :return:
        """
        svr_session = dlpx_obj.server_session
        disable_params = SourceDisableParameters()
        try:
            if self.group:
                vdb_container_obj = ref.find_db_by_name_and_group(
                    svr_session, self.group, self.name, False
                )
                vdb_obj = ref.find_source_obj_by_containerref(
                    svr_session, source, vdb_container_obj.reference
                )
            else:
                vdb_obj = ref.find_obj_by_name(svr_session, source, self.name)
            if self.force:
                disable_params.attempt_cleanup = False
                source.disable(svr_session, vdb_obj.reference, disable_params)
            else:
                source.disable(svr_session, vdb_obj.reference)
            self._add_last_job_to_track(dlpx_obj)
        except (
            exceptions.RequestError,
            exceptions.JobError,
            AttributeError,
        ) as err:
            log.print_exception(
                f"An error occurred while disabling dataset {self.name}: {err}"
            )
            # raise dxe.DlpxException(
            #     f"An error occurred while disabling dataset {self.name}:
            #     {err}"
            # )
            self.failures[0] = True

    def _list(self, dlpx_obj):
        """
        Lists all databases with stats for an engine
        """
        svr_session = dlpx_obj.server_session
        db_size = None
        active_space = None
        sync_space = None
        log_space = None
        try:
            all_source_objs = source.get_all(svr_session)
            all_consumer_objs = consumer.get_all(svr_session)
            for db_stats in all_consumer_objs:
                source_stats = ref.find_obj_list_by_containername(
                    all_source_objs, db_stats.container
                )
                if source_stats is not None:
                    active_space = (
                        db_stats.breakdown.active_space / 1024 / 1024 / 1024
                    )
                    sync_space = (
                        db_stats.breakdown.sync_space / 1024 / 1024 / 1024
                    )
                    log_space = db_stats.breakdown.log_space / 1024 / 1024
                    db_size = (
                        source_stats.runtime.database_size / 1024 / 1024 / 1024
                    )
                if source_stats.virtual is False:
                    print(
                        f"name: {db_stats.name}, provision container:"
                        f" {db_stats.parent}, disk usage: {db_size:.2f}GB,"
                        f"Size of Snapshots: {active_space:.2f}GB, "
                        f"dSource Size: {sync_space:.2f}GB, "
                        f"Log Size: {log_space:.2f}MB,"
                        f"Enabled: {source_stats.runtime.enabled},"
                        f"Status: {source_stats.runtime.status}"
                    )
                elif source_stats.virtual is True:
                    print(
                        f"name: {db_stats.name}, provision container: "
                        f"{db_stats.parent}, disk usage: "
                        f"{active_space:.2f}GB, Size of Snapshots: "
                        f"{sync_space:.2f}GB"
                        f"Log Size: {log_space:.2f}MB, Enabled: "
                        f"{source_stats.runtime.enabled}, "
                        f"Status: {source_stats.runtime.status}"
                    )
                elif source_stats is None:
                    print(
                        f"name: {db_stats.name},provision container: "
                        f"{db_stats.parent}, database disk usage: "
                        f"{db_size:.2f}GB,"
                        f"Size of Snapshots: {active_space:.2f}GB,"
                        "Could not find source information. This could be a "
                        "result of an unlinked object"
                    )
        except (
            exceptions.RequestError,
            AttributeError,
            dxe.DlpxException,
        ) as err:
            log.print_exception(
                f"An error occurred while listing databases: {err}"
            )
            self.failures[0] = True
        except (Exception) as err:
            log.print_exception(
                f"An error occurred while listing databases: {err}"
            )
            self.failures[0] = True

    @run_async
    def main_workflow(self, engine, dlpx_obj, single_thread):
        """
        This function is where we create our main workflow.
        Use the @run_async decorator to run this function asynchronously.
        The @run_async decorator to run multithreaded on Delphix Engines
        simultaneously
        :param engine: Dictionary of engines
        :type engine: dictionary
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param single_thread: True - run single threaded,
                               False - run multi-thread
        :type single_thread: bool
        """
        dlpx_obj = self._initialize_session()
        self._setup_dlpx_session(dlpx_obj, engine)
        if dlpx_obj.server_session:
            try:
                with dlpx_obj.job_mode(single_thread):
                    if self.action == VirtualOps.START:
                        self._start(dlpx_obj)
                    elif self.action == VirtualOps.STOP:
                        self._stop(dlpx_obj)
                    elif self.action == VirtualOps.ENABLE:
                        self._enable(dlpx_obj)
                    elif self.action == VirtualOps.DISABLE:
                        self._disable(dlpx_obj)
                    elif self.action == VirtualOps.LIST:
                        self._list(dlpx_obj)
                    run_job.track_running_jobs(
                        engine,
                        dlpx_obj,
                        poll=self.poll,
                        failures=self.failures,
                    )
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
                # raise err
                self.failures[0] = True
