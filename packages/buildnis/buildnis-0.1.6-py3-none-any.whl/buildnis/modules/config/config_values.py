# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_values.py
# Date:     01.Mar.2021
###############################################################################

from buildnis.modules.config import FilePath
from typing import List


# List of files and directories to delete if this has been called with
# `--distclean`.
g_list_of_generated_files: List[FilePath] = []
g_list_of_generated_dirs: List[FilePath] = []

# Defines global configuration values like the build project's root, version ...
# Most of this is configured in the project config file `project_config.json`.

PROJECT_ROOT: str = "./"
"""The root directory of the project, the directory `project_config.json` is 
located in.
"""

PROJECT_NAME: str = "Build Project"
"""The build project's name.
"""

PROJECT_VERSION: str = ""
"""The build project's name.
"""

PROJECT_AUTHOR: str = ""
"""The build project author's name(s).
"""

PROJECT_COMPANY: str = ""
"""The build project company's name.
"""

PROJECT_COPYRIGHT_INFO: str = ""
"""The build project's copyright info string.
"""

PROJECT_WEB_URL: str = ""
"""The build project's web URL.
"""

PROJECT_EMAIL: str = ""
"""The build project's email address.
"""

PROJECT_CONFIG_DIR_PATH: str = ""
"""The config path of the build project, the argument of `--generated-conf-dir` on the command line.
"""

# Host configuration, most of these are saved in the host configuration object `Host`.

HOST_OS: str = ""
"""The OS we are running on.
"""

HOST_NAME: str = "localhost"
"""The host's name.
"""

HOST_CPU_ARCH: str = ""
"""The host's CPU architecture, like `x64` or `x86`.
"""

HOST_NUM_CORES: int = 1
"""The number of physical cores of the host's CPU.
"""

HOST_NUM_LOG_CORES: int = 1
"""The number of logical cores (including Hyperthreading) cores of this host's CPU.
"""
