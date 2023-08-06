#
# Copyright (c) 2021 by Delphix. All rights reserved.
#
"""
Examples:
  dx_delete_vdb.py --vdb aseTest
  dx_delete_vdb.py --vdb aseTest --engine myengine
  --single_thread False --force
"""

from os.path import basename

from delphixpy.v1_10_2 import exceptions
from delphixpy.v1_10_2.web import database
from delphixpy.v1_10_2.web import vo
from dxi._lib import dlpx_exceptions
from dxi._lib import dx_logging
from dxi._lib import get_references
from dxi._lib import run_job
from dxi._lib.run_async import run_async
from dxi.dxi_tool_base import DXIBase


class DeleteConstants(object):
    """
    Define constants for Delete Class and CLI Usage
    """

    SINGLE_THREAD = False
    POLL = 20
    CONFIG = "config/dxtools.conf"
    LOG_FILE_PATH = "logs/dxi_delete.log"
    ENGINE_ID = "default"
    NAME = None
    PARALLEL = 5
    FORCE = False
    TYPE = None
    MODULE_NAME = __name__


class DXIDelete(DXIBase):
    """
    Deletes a VDB or a list of VDBs from an engine
    """

    def __init__(
        self,
        name=DeleteConstants.NAME,
        db_type=DeleteConstants.TYPE,
        force=DeleteConstants.FORCE,
        parallel=DeleteConstants.PARALLEL,
        engine=DeleteConstants.ENGINE_ID,
        poll=DeleteConstants.POLL,
        config=DeleteConstants.CONFIG,
        log_file_path=DeleteConstants.LOG_FILE_PATH,
        single_thread=DeleteConstants.SINGLE_THREAD,
        module_name=DeleteConstants.MODULE_NAME,
    ):
        """
        :param name: Colon[:] separated names of the VDBs/dSources to delete.
        :type name: `str`
        :param name: Type of object being deleted. vdb | dsource
        :type name: `str`
        :param parallel: Limit number of jobs to maxjob
        :type parallel: `int`
        :param engine: Alt Identifier of Delphix engine in dxtools.conf.
        :type engine: `str`
        :param poll: The number of seconds to wait between job polls
        :type poll: `int`
        :param config: The path to the dxtools.conf file
        :type config: `str`
        :param log_file_path: The path to the logfile you want to use.
        :type log_file_path: `str`
        :param single_thread: Run as a single thread.
            False if running multiple threads.
        :type single_thread: `bool`
        """
        super().__init__(
            parallel=parallel,
            poll=poll,
            config=config,
            log_file_path=log_file_path,
            single_thread=single_thread,
            module_name=module_name,
        )
        self.engine = engine
        self.name = name
        self.force = force
        self.db_type = db_type
        self.display_choices(self)
        self._validate_input()

    def _validate_input(self):
        if not self.name:
            dx_logging.print_exception(
                "Please provide the name of an object to delete. "
                "To provide a list of objects, separate them with colons.\n"
                "Eg  name1:name2"
            )
            raise
        if not self.db_type:
            dx_logging.print_debug(
                "Object type ( vdb or dsource ) not provided"
                "Defaulting to vdb."
            )
            self.db_type = "vdb"

    def delete_db(self):
        """
        Deletes the list of objects
        """
        try:
            for each in run_job.run_job_mt(
                self.main_workflow,
                self.dx_session_obj,
                self.engine,
                self.single_thread,
            ):
                each.join()
            elapsed_minutes = run_job.time_elapsed(self.time_start)
            dx_logging.print_info(
                f"Delete operation took {elapsed_minutes} minutes to "
                f"complete."
            )
            dx_logging.print_debug(">>> End Execution <<<")
            return True
        except Exception as err:
            dx_logging.print_exception(
                f"An Error was encountered during delete: {repr(err)}"
            )
            return False

    def _delete_database(self, dlpx_obj, datasets=None):
        """
        :param datasets: List containing datasets to delete
        :type datasets: `list`
        """
        for dataset in datasets:
            try:
                container_obj = get_references.find_obj_by_name(
                    dlpx_obj.server_session, database, dataset
                )
                # Check to make sure our container object has a reference
                source_obj = get_references.find_source_by_db_name(
                    dlpx_obj.server_session, dataset
                )
            except Exception as err:
                dx_logging.print_exception(
                    f"Unable to find a reference for {dataset} on "
                    f"engine {dlpx_obj.server_session.address}: {err}"
                )
                container_obj = None
            if container_obj.reference:
                if self.db_type != "vdb" or source_obj.virtual is not True:
                    dx_logging.print_exception(
                        f"Error : {dataset} is not a virtual object."
                    )
                    raise dlpx_exceptions.DlpxException(
                        f"Error : {dataset} is not a virtual object. "
                    )
                elif self.db_type == "dsource" and (
                    source_obj.linked is True or source_obj.staging is True
                ):
                    dx_logging.print_warning(
                        f"DELETING {dataset} THAT "
                        f"IS EITHER A SOURCE OR STAGING DATASET."
                    )
                elif self.db_type not in ['vdb', 'dsource']:
                    dx_logging.print_exception(
                        f"Error : {dataset} is not the "
                        f"provided type: {self.db_type}"
                    )
                    raise dlpx_exceptions.DlpxException(
                        f"Error : {dataset} is not the "
                        f"provided type: {self.db_type}"
                    )
                dx_logging.print_debug(
                    f"Deleting {dataset} on engine "
                    f"{dlpx_obj.server_session.address}"
                )
                delete_params = None
                if self.force and str(container_obj.reference).startswith(
                    "MSSQL"
                ):
                    delete_params = vo.DeleteParameters()
                    delete_params.force = True
                try:
                    dx_logging.print_debug(f"Deleting dataset : {dataset}")
                    database.delete(
                        dlpx_obj.server_session,
                        container_obj.reference,
                        delete_params,
                    )
                    self._add_last_job_to_track(dlpx_obj)
                except (
                        dlpx_exceptions.DlpxException,
                        exceptions.RequestError,
                        exceptions.HttpError,
                ) as err:
                    raise dlpx_exceptions.DlpxException(f"{err}")

    def _delete_helper(self, dlpx_obj):
        """
        :param dlpx_obj: Object that containers Delphix Engine information
                        along with session to access the current engine
        :type dlpx_obj: `lib.GetSession.GetSession`
        """
        database_lst = self.name.split(":")
        self._delete_database(dlpx_obj, datasets=database_lst)

    @run_async
    def main_workflow(self, engine, dlpx_obj, single_thread):
        """
        This function is where we create our main workflow.
        Use the @run_async decorator to run asynchronously.
        The @run_async decorator allows us to run
        against multiple Delphix Engines simultaneously
        :param engine: Dictionary of engines
        :type engine: dictionary
        :param dlpx_obj: DDP session object
        :type dlpx_obj: lib.GetSession.GetSession object
        :param single_thread:
            True - run single threaded,
            False - run multi-thread
        :type single_thread: bool
        """
        dlpx_obj = self._initialize_session()
        self._setup_dlpx_session(dlpx_obj, engine)
        try:
            with dlpx_obj.job_mode(single_thread):
                self._delete_helper(dlpx_obj)
                run_job.track_running_jobs(
                    engine, dlpx_obj, poll=self.poll, failures=self.failures
                )
        except (
            dlpx_exceptions.DlpxException,
            dlpx_exceptions.DlpxObjectNotFound,
            exceptions.RequestError,
            exceptions.JobError,
            exceptions.HttpError,
            Exception,
        ) as err:
            dx_logging.print_exception(
                f"Error in {basename(__file__)} on Delpihx Engine: "
                f'{engine["hostname"]} : {repr(err)}'
            )
            self.failures[0] = True
            # TODO: Add Exception to dictionary
