# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     check.py
# Date:     16.Feb.2021
###############################################################################

from __future__ import annotations

import os
import sys
import json
import pathlib
from typing import Any
from types import SimpleNamespace

from buildnis.modules import EXT_ERR_DIR, MODULE_DIR_PATH
from buildnis.modules.config.json_base_class import JSONBaseClass
from buildnis.modules.helpers.execute import doesExecutableWork, runCommand
from buildnis.modules.config import (
    Arch,
    BUILD_TOOL_CONFIG_NAME,
    CONFIGURE_SCRIPTS_PATH,
    LINUX_OS_STRING,
    OSName,
    OSX_OS_STRING,
)


class Check(JSONBaseClass):
    """Checks if all build tools are present.

    Runs all build tool script_paths in `configure_script_paths` in the subdirectory
    with the name of the OS passed to the constructor.

    Each build tool configuration (item of build_tool_cfgs) has the following
    attributes:

    * `name`                The name of the build tool
    * `name_long`           The full name of the build tool
    * `version`             The version of the build tool, gathered from its output
    * `version_arg`         The argument to call the build tool with to get the version
    * `version_regex`       The regex to parse the output of `version_arg` to get `version`
    * `build_tool_exe`      The executable's file name
    * `install_path`        The path to the executable
    * `env_script`          The environment script to call before using the executable
    * `env_script_arg`      The argument to call the environment script with
    * `is_checked`          Has the executable been run and the version output been parsed?

    Attributes:
        os_name (OSName): the OS we are building for
        arch (Arch): the CPU architecture we are building for
        build_tool_cfgs (list): the list of build tool configurations returned from
                        the script_paths in `configure_script_paths/OS`

    Methods:
        isBuildToolCfgOK: checks if the build tool config has the minimum
                            needed attributes
        checkVersions: runs all build tools with the version argument, to check
                        if the executable works
    """

    ###########################################################################
    def __init__(self, os_name: OSName, arch: Arch) -> None:
        """Constructor of Check, runs all build tool script_paths in
        `configure_script_paths`.

        All build tool script_paths in the `os` subdirectory of `configure_script_paths`
        are run, the CPU architecture `arch` is passed as an argument to each
        script_path.

        Args:
            os_name (OSName): the OS we are building for
            arch (Arch): the CPU architecture we are building for
        """
        super().__init__(
            config_file_name=BUILD_TOOL_CONFIG_NAME, config_name="build tools"
        )

        self.os = os_name
        self.arch = arch        

        working_dir = pathlib.Path(
            os.path.normpath("/".join([CONFIGURE_SCRIPTS_PATH, os_name]))
        )
        if not working_dir.is_dir():
            self._logger.critical(
                'error calling build tool scripts, "\{path}" does not exist or is not a directory!'.format(
                    path=working_dir
                )
            )
            sys.exit(EXT_ERR_DIR)

        self.build_tool_cfgs = []
        for script_path in working_dir.glob("*"):
            try:
                if script_path.is_file():

                    self._logger.warning(
                        'Calling build tool config script "{path}"'.format(
                            path=script_path
                        )
                    )
                    try:
                        script_out = runCommand(exe=script_path, args=[self.arch])

                        build_tool_cfg = json.loads(
                            script_out.std_out,
                            object_hook=lambda dict: SimpleNamespace(**dict),
                        )

                    except Exception as excp:
                        self._logger.error(
                            'error "{error}" running build tool script "{path}"'.format(
                                error=excp, path=script_path
                            )
                        )

                    for item in build_tool_cfg.build_tools:
                        if self.isBuildToolCfgOK(item):
                            self.build_tool_cfgs.append(item)
                        else:
                            self._logger.error(
                                'build tool config "{cfg}" doesn\'t have all needed attributes!'.format(
                                    cfg=script_path
                                )
                            )
            except Exception as excp:
                self._logger.error(
                    'build tool filename "{cfg}" not valid'.format(cfg=script_path)
                )

        self.checkVersions()

    ############################################################################
    def isBuildToolCfgOK(self, cfg: Any) -> bool:
        """Checks if the given object has all the needed attributes of a build
        tool configuration.

        Args:
            cfg (obj): the object to check

        Returns:
            bool: True, if `cfg` has all needed attributes
                  False else
        """
        # TODO add 'provides' (like "C++", "Java", "Python")
        must_have_attrs = ["name", "build_tool_exe", "version_regex"]

        for attr in must_have_attrs:
            if not hasattr(cfg, attr):
                self._logger.error(
                    'build config has no attribute "{name}"'.format(name=attr)
                )
                return False

        attribute_list = [
            "name_long",
            "version",
            "install_path",
            "env_script",
            "env_script_arg",
            "version_arg",
        ]
        for attribute in attribute_list:
            if not hasattr(cfg, attribute):
                setattr(cfg, attribute, "")

        return True

    ############################################################################
    def checkVersions(self) -> None:
        """Runs all configured build tools with the 'show version' argument.

        To check, if the configured build tools exist and are working, try to
        execute each with the argument to get the version string of the build
        tool.
        """
        for tool in self.build_tool_cfgs:
            if tool.build_tool_exe == "":
                self._logger.error(
                    'build tool "{name}" has no executable configured!'.format(
                        name=tool.name
                    )
                )
                continue

            exe_path = tool.build_tool_exe

            # has environment script to call
            if tool.env_script != "":
                self._logger.info(
                    '"{name}": calling environment script "{script}".'.format(
                        name=tool.name, script=tool.env_script
                    )
                )

            # has full path (so maybe not in PATH)
            elif tool.install_path != "":
                exe_path = os.path.normpath(
                    "/".join([tool.install_path, tool.build_tool_exe])
                )
                self._logger.info(
                    '"{name}": using path "{path}".'.format(
                        name=tool.name, path=exe_path
                    )
                )

            # no full path given, so it hopefully is in PATH
            else:
                self._logger.info(
                    '"{name}": checking if executable "{exe}" is in PATH.'.format(
                        name=tool.name, exe=tool.build_tool_exe
                    )
                )

            try:
                if self.os == LINUX_OS_STRING or self.os == OSX_OS_STRING:
                    source_env_script = True
                else:
                    source_env_script = False
                tool.version = doesExecutableWork(
                    exe=exe_path,
                    check_regex=tool.version_regex,
                    regex_group=1,
                    args=[tool.version_arg],
                    env_script=tool.env_script,
                    env_script_args=[tool.env_script_arg],
                    source_env_script=source_env_script,
                )
                if tool.version != "":
                    tool.is_checked = True

            except Exception as excp:
                self._logger.error(
                    'error "{error}" parsing version of "{exe} {opt}" using version regex "{regex}"'.format(
                        error=excp,
                        exe=exe_path,
                        opt=tool.version_arg,
                        regex=tool.version_regex,
                    )
                )
