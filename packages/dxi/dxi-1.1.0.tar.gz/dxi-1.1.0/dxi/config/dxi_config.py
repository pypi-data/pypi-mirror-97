#
# Copyright (c) 2021 by Delphix. All rights reserved.
#
"""
This module includes classes for
dxi configuration related operations.
"""
import json

from dxi._lib import dlpx_exceptions as dxe
from dxi._lib import dx_logging as log
from dxi._lib import util


class DXIConfigConstants(object):
    """
    Define constants for Config Operations.
    """

    CONFIG = "config/dxtools.conf"
    LOG_FILE_PATH = "logs/dxi_config.log"
    MODULE_NAME = __name__


class DXIConfig:
    """
    Class for dxi config related opertaions.
    """

    def __init__(
        self,
        config=DXIConfigConstants.CONFIG,
        log_file_path=DXIConfigConstants.LOG_FILE_PATH,
    ):
        """
        :param config: The path to the dxtools.conf file
        :type config: `str`

        :param log_file_path: The path to the logfile for this module
        :type log_file_path: `str`
        """
        self.config = util.find_config_path(config)
        self.log_file_path = util.find_log_path(
            log_file_path, DXIConfigConstants.MODULE_NAME
        )
        self.module_name = (__name__,)
        self.key = ""

    def _encryption_helper(self):
        """
        Helper for encrypt operation
        """
        try:
            with open(self.config) as config_file:
                config = json.loads(config_file.read())
        except IOError as err:
            err_msg = (
                f"\nERROR: Unable to open {config_file}. Please "
                f"check the path, permissions and retry: {err}"
            )
            log.print_exception(err_msg)
            raise dxe.DlpxException(err_msg)
        except (ValueError, TypeError, AttributeError) as err:
            err_msg = (
                f"\nERROR: Unable to read {config_file} as json."
                f"Please check if the file is in a json format and retry:{err}"
            )
            log.print_exception(err_msg)
            raise dxe.DlpxException(err_msg)
        try:
            for each in config.keys():
                temp_config = config[each]
                temp_config["hostname"] = each
                self.key = util.get_encryption_key(temp_config["ip_address"])
                try:
                    if temp_config["encrypted"].lower() == "true":
                        isEncrypted = True
                    else:
                        isEncrypted = False
                except Exception:
                    isEncrypted = False
                if not isEncrypted:
                    temp_config["username"] = util.encrypt_data(
                        self.key, temp_config["username"]
                    )
                    temp_config["password"] = util.encrypt_data(
                        self.key, temp_config["password"]
                    )
                    temp_config["encrypted"] = "true"
                config[each] = temp_config
                with open(self.config, "w") as encrypt_file:
                    json.dump(config, encrypt_file, indent=4)
        except (Exception) as err:
            log.print_exception(
                f"Error: "
                f"There was an error while encrypting {self.config}\n {err}"
            )
            raise

    def encrypt(self):
        """
        Encrypt username and password information in the dxi config file.
        """
        try:
            log.logging_est(self.log_file_path)
            log.print_info(f"Starting encryption of file:{self.config}")
            self._encryption_helper()
            log.print_info(f"Encryption of file:{self.config} successful")
            return True
        except Exception:
            return False
