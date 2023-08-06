# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     20.Feb.2021
###############################################################################

__all__ = [
    "parseCommandLine",
    "CommandlineArguments",
    "LOGGER_NAME",
    "getProgramLogger",
    "FileCompare",
    "FileCompareException",
    "hashFile",
    "areHashesSame",
    "checkIfExists",
    "checkIfIsFile",
    "checkIfIsDir",
    "checkIfIsLink",
    "makeDirIfNotExists",
    "runCommand",
    "doesExecutableWork",
    "ExecuteException" "getJSONDict",
    "writeJSON",
    "readJSON",
    "WebException",
    "doDownload",
]

LOGGER_NAME = "Buildnis"
