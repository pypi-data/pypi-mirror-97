# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     logging.py
# Date:     20.Feb.2021
###############################################################################

import logging
from buildnis.modules.config import FilePath
from buildnis.modules.helpers import LOGGER_NAME
import sys

################################################################################
def getProgramLogger(level: int, logfile: FilePath) -> logging.Logger:
    """Returns the logger to use for the program.

    Always logs `DEBUG`, `INFO` and `WARNING` to `stdout`,
    `ERROR` and `CRITICAL` go to `stderr`. If a `logfile` is given, everything
    is logged to this file too.
    `level` is the minimum log level to actually output messages.

    When you want to use this logger, simply call

        my_logger = modules.helpers.logging.getProgramLogger()

        my_logger.info ("Info level log")
        my_logger.error ("Error level log")

    Args:
        level (int): minimumm log level to output
        logfile (FilePath): if this is not `None` or the empty string
                            `""`, log to this file too.

    Returns:
        logging.Logger: the `logging.Logger` instance to use to log
    """
    ret_val = logging.getLogger(LOGGER_NAME)

    ret_val.setLevel(logging.DEBUG)

    stdout_hdl = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(message)s")
    stdout_hdl.setFormatter(formatter)
    stdout_hdl.addFilter(lambda lvl: lvl.levelno < logging.ERROR)
    stdout_hdl.setLevel(level)
    ret_val.addHandler(stdout_hdl)

    stderr_hdl = logging.StreamHandler(sys.stderr)
    err_formatter = logging.Formatter("%(levelname)s: %(message)s")
    stderr_hdl.setFormatter(err_formatter)
    stderr_hdl.setLevel(logging.ERROR)
    ret_val.addHandler(stderr_hdl)

    if logfile != "" and logfile != None:
        file_hdl = logging.FileHandler(logfile, mode="w")
        file_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s", datefmt="%d.%m.%Y %H:%M:%S"
        )
        file_hdl.setFormatter(file_formatter)
        file_hdl.setLevel(logging.DEBUG)
        ret_val.addHandler(file_hdl)

    return ret_val
