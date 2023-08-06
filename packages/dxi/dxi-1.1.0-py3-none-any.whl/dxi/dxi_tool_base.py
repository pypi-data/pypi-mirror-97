#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import time
from abc import ABC
from os.path import basename

from dxi._lib import dlpx_exceptions
from dxi._lib import dx_logging
from dxi._lib import get_session
from dxi._lib import run_job
from dxi._lib import util


class DXIBase(ABC):
    """
    This class cannot be directly instantiated as it is abstract class.
    It also contains common properties like poll, single_thread etc.
    """

    def __init__(
        self,
        poll,
        config,
        log_file_path,
        single_thread,
        module_name,
        engine=None,
        parallel=5,
    ):
        self.parallel = parallel
        self.poll = poll
        self.single_thread = single_thread
        self.module_name = module_name
        self.config = util.find_config_path(config)
        self.engine = engine
        self.log_file_path = util.find_log_path(log_file_path, module_name)
        self.dx_session_obj = self._initialize_session()
        self.time_start = time.time()
        self.failures = [False]
        dx_logging.logging_est(self.log_file_path)

    def _initialize_session(self):
        dx_session_obj = get_session.GetSession()
        dx_session_obj.get_config(config_file_path=self.config)
        return dx_session_obj

    def display_choices(self, obj):
        dx_logging.print_debug("-" * 79)
        dx_logging.print_debug("Provided parameters for execution")
        dx_logging.print_debug("-" * 79)
        attrs = vars(obj)
        pw_keys = [
            key
            for key, value in attrs.items()
            if ("pass" in key.lower() or "user" in key.lower())
        ]
        for pw_key in pw_keys:
            attrs[pw_key] = "*" * 10
        dx_logging.print_debug(
            "\n ".join("%s: %s" % item for item in attrs.items())
        )
        dx_logging.print_debug("-" * 79)

    def _execute_operation(self, function_ref):
        """
        :param function_ref: A function reference
        :type function_ref: `callable`
        """
        try:
            for each in run_job.run_job_mt(
                function_ref,
                self.dx_session_obj,
                self.engine,
                self.single_thread,
            ):
                each.join()

            if self.failures[0] is True:
                raise
        except Exception as err:
            dx_logging.print_exception(err)
            raise
        elapsed_minutes = run_job.time_elapsed(self.time_start)
        dx_logging.print_info(
            f"script took {elapsed_minutes} minutes to complete"
        )

    @staticmethod
    def _setup_dlpx_session(dlpx_obj, engine_ref):
        """
        :param dlpx_obj: DDP session object
        :type dlpx_obj: `lib.GetSession.GetSession`
        :param engine_ref: Dictionary of engines
        :type engine_ref: `dict`
        """
        try:
            # Setup the connection to the Delphix DDP
            dx_logging.print_debug("Setting up the dlpx session")
            dlpx_obj.dlpx_session(
                engine_ref["ip_address"],
                engine_ref["username"],
                engine_ref["password"],
                engine_ref["use_https"],
            )
            dx_logging.print_debug("Connection established")
        except (dlpx_exceptions.DlpxException, Exception) as err:
            dx_logging.print_exception(
                f"ERROR: {basename(__file__)} encountered an error "
                f"authenticating"
                f' to {engine_ref["hostname"]} {err}'
            )
            raise dlpx_exceptions.DlpxException(
                f"ERROR: {basename(__file__)} encountered an error "
                f"authenticating"
                f' to {engine_ref["hostname"]} {err}'
            )

    @staticmethod
    def _add_last_job_to_track(dlpx_obj):
        if dlpx_obj.server_session.last_job:
            if dlpx_obj.server_session.address in dlpx_obj.jobs:
                dlpx_obj.jobs[dlpx_obj.server_session.address].append(
                    dlpx_obj.server_session.last_job
                )
            else:
                dlpx_obj.jobs[dlpx_obj.server_session.address] = [
                    dlpx_obj.server_session.last_job
                ]
