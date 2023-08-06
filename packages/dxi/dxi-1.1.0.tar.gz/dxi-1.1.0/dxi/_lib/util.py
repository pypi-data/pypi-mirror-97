#
# Copyright (c) 2021 by Delphix. All rights reserved.
#

import base64
import os
import sys
import json
import uuid

from delphixpy import exceptions
from dxi._lib import dlpx_exceptions
from . import dx_logging as log

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet



def find_config_path(config_file_path):
    """
    Locate the config path if the default is passed.

    :param config_file_path: Path to the configuration file.
    :type config_file_path: `str`
    :return: config_file_path
    :rtype: `str`
    """
    if not os.path.isfile(config_file_path):
        if "dxtools.conf" == config_file_path.split("/")[-1]:
            config_file_path = str(
                os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "config/dxtools.conf",
                )
            )
        else:
            raise Exception("Failed to find config path")
    log.print_info("Config file path is: {}".format(config_file_path))
    return config_file_path


def find_log_path(log_path, module_name):
    """
    Locate the log path if the default is passed.
    This logic will be changed once log_path is property of parent class.

    :param config_file_path: Path to the configuration file.
    :type config_file_path: `str`
    :param module_name: Module name
    :type module_name: `str`
    :return: Log file path
    :rtype: `str`
    """

    try:
        if not os.path.isfile(log_path):
            path = "logs/" + module_name.split(".")[-1] + ".log"
            log_path = str(
                os.path.join(os.path.dirname(__file__),  "..", path)
            )
            log.print_info("Log file path is: {}".format(log_path))
        return log_path
    except Exception as err:
        raise Exception("Failed to find log path {}".format(repr(err)))


def run_async(func):
    """
    http://code.activestate.com/recipes/576684-simple-threading-decorator/
    run_async(func)
    function decorator, intended to make "func" run in a separate
    thread (asynchronously).
    Returns the created Thread object

    E.g.:
    @run_async
    def task1():
        do_something

    @run_async
    def task2():
        do_something_too

        t1 = task1()
        t2 = task2()
        ...
        t1.join()
        t2.join()

    :param func: The callable function object to be invoked by the run
    :type func: `callable`
    :return: Decorated function
    :rtype: `callable`

    """
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def exception_handler(function):
    def inner_function(*args, **kwargs):
        try:
            function(*args, **kwargs)
            # Here we handle what we do when the unexpected happens
            return True
        except SystemExit as err:
            # This is what we use to handle our sys.exit(#)
            log.print_exception(
                f"ERROR: Please check the ERROR message below:\n{err}"
            )
        except dlpx_exceptions.DlpxException as err:
            # We use this exception handler when an error occurs in a function.
            log.print_exception(
                f"ERROR: Please check the ERROR message below:\n{err}"
            )
        except exceptions.HttpError as err:
            # We use this exception handler when our connection to Delphix
            # fails
            print(
                f"ERROR: Connection failed to the Delphix Engine. Please "
                f"check the error message below:\n{err}"
            )
        except exceptions.JobError as err:
            # We use this exception handler when a job fails in Delphix so
            # that we have actionable data
            print(f"A job failed in the Delphix Engine:\n{err.job}")
        except KeyboardInterrupt:
            # We use this exception handler to gracefully handle ctrl+c exits
            log.print_debug(
                "You sent a CTRL+C to interrupt the process"
            )
        return False

    return inner_function


def convert_dct_str(obj_dct):
    """
    Convert dictionary into a string for printing
    :param obj_dct: Dictionary to convert into a string
    :type obj_dct: dict
    :return: string object
    """
    js_str = ""
    if isinstance(obj_dct, dict):
        for js_db, js_jdbc in obj_dct.items():
            if isinstance(js_jdbc, list):
                js_str += f'{js_db}: {", ".join(js_jdbc)}\n'
            elif isinstance(js_jdbc, str):
                js_str += f"{js_db}: {js_jdbc}\n"
    else:
        raise dlpx_exceptions.DlpxException(
            f"Passed a non-dictionary object to convert_dct_str():"
            f"{type(obj_dct)}"
        )
    return js_str


def boolean_based_system_exit(bool_status):
    """
    Exit with correct code based on boolean value
    :param bool_status:
    :type bool_status
    """
    if bool_status:
        sys.exit(0)
    else:
        sys.exit(1)


def show_progress(per, jobid, with_progress_bar=True, status='Running', total=100):
    if with_progress_bar:
        prefix = 'Progress(' + jobid + ')'
        if per >= total:
            status = 'Completed'
        bar_len = 60
        filled_len = int(round(per * bar_len / float(total)))
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        fmt = f'\r{prefix} |{bar}| {per}% {status}'
        print('\b' * len(fmt), end='')
        sys.stdout.write(fmt)
        sys.stdout.flush()


def decrypt_data(key, value):
    """
    Decryts a value with SHA265 agorithm
    :param value: value to decrypt
    return decrypted value
    """
    hashhex = value[-64:]
    enc = value[0:-64]
    try:
        dehex = bytes.fromhex(enc)
        msg_nonce = dehex[:12]
        ciphertext = dehex[12:]
        cipher = ChaCha20Poly1305(key)
        value = cipher.decrypt(msg_nonce, ciphertext, None)
        hash_object = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_object.update(value)
        dhash = hash_object.finalize()
        hashhex_check = dhash.hex()
        if hashhex == hashhex_check:
            return value.decode('utf-8')
        else:
            raise Exception("Password SHA256 value after decrypt is wrong")
    except InvalidTag as err:
        log.print_exception(f"Wrong decryption key: {err}")
        raise err
    except Exception as err:
        log.print_exception(f"Error: Incorrect Decrypted Value: {err}")
        raise err

def encrypt_data(key,password):
    """
    Encrypts a value with SHA 256 algorithm
    :param value : Value to encrypt
    return encryted value
    """
    try:
        hash_object = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hash_object.update(password.encode())
        dhash = hash_object.finalize()
        hashhex = dhash.hex()
        nonce = os.urandom(12)
        cipher = ChaCha20Poly1305(key)
        enc = cipher.encrypt(nonce, password.encode(), None)
        enchex = enc.hex()
        return nonce.hex() + enchex + hashhex
    except Exception as err:
        log.print_exception(f"Error: There as an exception while encrypting {err}")
        raise err

def get_encryption_key(seed):
    try:
        key = hex(uuid.getnode())+seed
        key = '{:32.32}'.format(key)
        key = key.encode()
        return key
    except Exception as err:
        log.print_exception(f"Error: There was an error creating key: {err}")
        raise
