# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     build_tool.py
# Date:     05.Mar.2021
###############################################################################

from __future__ import annotations
from buildnis.modules.config import BUILD_FILE_NAME, FilePath

from buildnis.modules.helpers.files import FileCompare, returnExistingFile
from buildnis.modules.config.json_base_class import JSONBaseClass


class BuildCfg(JSONBaseClass):
    """Holds a build tool configuration read from a JSON build tool
    configuration file.

    Methods:
        fromReadJSON: Converts the `SimpleNamespace` instance read from a JSON
                        file to a BuildCfg instance to use.
        writeJSON: Writes the configuration to file (not used, because it is
                    part of the project configuration JSON file).
    """

    ###########################################################################
    def __init__(
        self, build_config: FilePath, json_path: FilePath, load_json: bool = True
    ):
        """Loads the file from one of the given JSON paths.

        If `json_path` exists, it is loaded from this file, else `build_config`
        is read.

        Args:
            build_config (FilePath): The path to the original JSON build
                                    configuration  file.
            json_path (FilePath): The path where the parsed build tool configuration
                                    should be saved to. It is not used, because
                                    the `BuildCfg` instances are part of the
                                    project configuration file.
            load_json (bool, optional): Should the configuration be read from the
                                    file `build_config`. Defaults to True.
        """
        super().__init__(config_file_name=BUILD_FILE_NAME, config_name="build")

        self.config_path = build_config
        self.json_path = json_path

        if load_json:
            read_config_path = returnExistingFile([self.json_path, self.config_path])

            self.readJSON(json_path=read_config_path)

            must_have_attrs = {
                "name": "",
                "build_type": "",
                "build_subtype": "",
                "build_tool_type": "",
                "os": [],
                "stages": [],
            }
            for attr in must_have_attrs:
                if not hasattr(self, attr):
                    setattr(self, attr, must_have_attrs[attr])

    ############################################################################
    @classmethod
    def fromReadJSON(cls, instance: object) -> BuildCfg:
        """Converts a `SimpleNamespace` instance load from a JSON build tools
        configuration file to a BuildCfg instance to use.

        Args:
            instance (object): The `Simplenamespace` instance to convert.

        Returns:
            BuildCfg: The data of the given object as a `BuildCfg` instance.
        """
        ret_val = cls(
            build_config=instance.config_path,
            json_path=instance.json_path,
            load_json=False,
        )

        for item in instance.__dict__:
            setattr(ret_val, item, instance.__dict__[item])

        ret_val.orig_file = FileCompare(ret_val.orig_file.path)
        ret_val.orig_file.size = instance.orig_file.size
        ret_val.orig_file.hash = instance.orig_file.hash

        return ret_val

    ##############################################################################
    def writeJSON(self) -> None:
        """Writes the generated config to disk.

        Not used, because it is part of the project configuration file.
        """
        super().writeJSON(json_path=self.json_path)
