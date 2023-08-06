# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     __init__.py
# Date:     13.Feb.2021
###############################################################################

__all__ = [
    "Config",
    "Host",
    "Check",
    "ProgramDependency",
    "PROJECT_FILE_NAME",
    "PROGRAM_DEP_FILE_NAME",
    "MODULE_FILE_NAME",
    "BUILD_FILE_NAME",
    "HOST_FILE_NAME",
    "BUILD_TOOL_CONFIG_NAME",
    "CFG_DIR_NAME" "CFG_VERSION",
    "DEFAULT_CONFIG_FILE",
    "CONFIGURE_SCRIPTS_PATH",
    "WINDOWS_OS_STRING",
    "LINUX_OS_STRING",
    "OSX_OS_STRING",
    "AMD64_ARCH_STRING",
    "I86_ARCH_STRING",
    "OSX_NAME_DICT",
    "config_values",
    "ConfigDirJson",
    "JSONBaseClass",
    "ModuleCfg",
    "BuildCfg",
]

import collections
from typing import NamedTuple

from buildnis.modules import MODULE_DIR_PATH

# Types to use for type hints

ConfigVersion = collections.namedtuple("Version", ["major", "minor"])
CFG_VERSION = ConfigVersion(major="1", minor="0")

FilePath = str

OSName = str

Arch = str


class CmdOutput(NamedTuple):
    """The return type of executed commands.

    Attributes:
        std_out (str): the `stdout` output of the executed command
        err_out (str): the `stderr` output of the executed command
    """

    std_out: str = ""
    err_out: str = ""


OSX_NAME_DICT = {
    "10.0": "Cheetah",
    "10.1": "Puma",
    "10.2": "Jaguar",
    "10.3": "Panther",
    "10.4": "Tiger",
    "10.5": "Leopard",
    "10.6": "Snow Leopard",
    "10.7": "Lion",
    "10.8": "Mountain Lion",
    "10.9": "Mavericks",
    "10.10": "Yosemite",
    "10.10": "El Capitan",
    "10.12": "Sierra",
    "10.13": "High Sierra",
    "10.14": "Mojave",
    "10.15": "Catalina",
    "11.0": "Big Sur",
    "11.1": "Big Sur",
    "11.2": "Big Sur",
}

# Constants to use for JSON files, arguments, ...
DEFAULT_CONFIG_FILE = "./project_config.json"

PROJECT_DEP_FILE_NAME = "project_dependency_config"

PROJECT_FILE_NAME = "project_config"

MODULE_FILE_NAME = "module_config"

BUILD_FILE_NAME = "build_config"

CFG_DIR_NAME = "cfg_dir_config"

HOST_FILE_NAME = "host_config"

WINDOWS_OS_STRING = "Windows"

LINUX_OS_STRING = "Linux"

OSX_OS_STRING = "OSX"

AMD64_ARCH_STRING = "x64"

I86_ARCH_STRING = "x86"

CONFIGURE_SCRIPTS_PATH = "/".join([MODULE_DIR_PATH, "./configure_scripts"])

BUILD_TOOL_CONFIG_NAME = "build_tool_config"

BUILD_CONF_PATH = "./build_conf"
