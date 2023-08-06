#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import logging

import click

logger = logging.getLogger(__name__)


def logging_est(logfile_path, debug=False):
    """
    Establish Logging

    :param logfile_path: path to the logfile. Default: current directory.
    :type logfile_path: str
    :param debug: Set debug mode on (True) or off (False).
    :type debug: bool
    """
    logging.basicConfig(
        filename=logfile_path,
        format="%(levelname)s:%(asctime)s:%(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger()
    if debug is True:
        logger.setLevel(20)
        print_info("Debug Logging is enabled.")
    print_info("Logging Started")


def print_debug(print_obj):
    """
    Call this function with a log message to prefix the message with DEBUG
    :param print_obj: Object to print to logfile and stdout
    :type print_obj: type depends on objecting being passed. Typically str
    """

    # Uncomment below line if want more detailed logs on console.
    # It would be better if we can provide an option to user to send debug flag.

    #click.secho(f"DEBUG: {str(print_obj)}", fg="green")
    logger.debug(str(print_obj))


def print_info(print_obj):
    """
    Call this function with a log message to prefix the message with INFO
    :param print_obj: Object to print to logfile and stdout
    :type print_obj: type depends on objecting being passed. Typically str
    """
    click.secho(f"INFO: {print_obj}", fg="blue")
    logger.info(str(print_obj))


def print_warning(print_obj):
    """
    Call this function with a log message to prefix the message with INFO
    :param print_obj: Object to print to logfile and stdout
    :type print_obj: type depends on objecting being passed. Typically str
    """
    click.secho(f"WARN: {print_obj}", fg="yellow", bg="white")
    logger.warning(str(print_obj))


def print_exception(print_obj):
    """
    Call this function with a log message to prefix the message with EXCEPTION
    :param print_obj: Object to print to logfile and stdout
    :type print_obj: type depends on objecting being passed. Typically str

    """
    click.secho(str(print_obj), fg="red")
    logger.error("EXCEPTION: %s" % (str(print_obj)))
