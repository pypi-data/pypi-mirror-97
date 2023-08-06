# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     json_base_class.py
# Date:     02.Mar.2021
###############################################################################

from __future__ import annotations

import pprint
import logging
import sys
from typing import Dict, List

from buildnis.modules.helpers.config_parser import parseConfigElement
from buildnis.modules import EXT_ERR_LD_FILE
from buildnis.modules.helpers.json import getJSONDict, readJSON, writeJSON
from buildnis.modules.config import CFG_VERSION, FilePath
from buildnis.modules.helpers import LOGGER_NAME


class JSONBaseClass:
    """Base class for all objects that read and/or write JSON configuration
    files.
    Holds the values of the JSON file in it'S attributes (all except
    `_logger`, the `loggin.Logger` instance).

    Methods:
        hasConfigChangedOnDisk: Returns `True` if the JSON configuration has
                                changed since the time the checksum has been
                                calculated.
        expandAllPlaceholders: Replaces all placeholders (like `${PLACEHOLDER}`)
                                in the instance's attribute values.
        readJSON: Reads the JSON config file and saves the values to attributes.
        reReadIfChangedOnDisk: Checks if the original read file has changed on
                                disk, and if yes, rereads the file from disk.
        writeJSON: Writes the attributes and their values to the JSON file.
        reWriteIfChangedOnDisk: Checks if the original read file has changed on
                                disk, and if yes, rereads the file from disk
                                and rewrites it to the generated JSON's file
                                path.
    """

    ###########################################################################
    def __init__(self, config_file_name: str, config_name: str) -> None:
        """Sets the config file's name to `config_file_name` and the internal
        file name to `config_name`.

        Args:
            config_file_name (str): The 'nice', human readable, name of the
                                    config file
            config_name (str): The internal name of the configuration file,
                                also saved as element in the JSON file to
                                check the validity.
        """
        self.file_name = config_file_name
        self.config_name = config_name
        self.file_version = ".".join(CFG_VERSION)
        self._logger = logging.getLogger(LOGGER_NAME)

    ############################################################################
    def readJSON(self, json_path: FilePath) -> None:
        """Reads a JSON file and puts it's items into attributes of this object.

        Args:
            json_path (FilePath): The path of the JSON file to load.
        """
        try:
            tmp_obj = readJSON(
                json_path=json_path,
                file_text=self.config_name,
                conf_file_name=self.file_name,
            )

            for item in tmp_obj.__dict__:
                if isinstance(item, str):
                    setattr(self, item, tmp_obj.__dict__[item])
                else:
                    self._logger.error(
                        'error reading file "{file}": found item "{item}" in object dictionary that isn\'t a string!'.format(
                            file=json_path, item=item
                        )
                    )
        except Exception as excp:
            self._logger.critical(
                'error "{error}" reading JSON file "{json_path}"'.format(
                    error=excp, json_path=json_path
                )
            )
            sys.exit(EXT_ERR_LD_FILE)

    ############################################################################
    def expandAllPlaceholders(self, parents: List[object] = []) -> None:
        """Goes through all configurations and replaces placeholders in their
        elements. A Placeholder is a string like `${PLACEHOLDER}`, a dollar
        sign followed by a curly opening brace, the string to replace and the
        closing curly brace.

        See also: `modules.helpers.config_parser.parseConfigElement`

        Args:
            parents (List[object]): The hierarchical list of parent objects.
        """
        local_parents = parents.copy()
        local_parents.append(self)
        tmp_obj = parseConfigElement(element=self, parents=local_parents)

        for item in tmp_obj.__dict__:
            if isinstance(item, str):
                setattr(self, item, tmp_obj.__dict__[item])
            else:
                self._logger.error(
                    'error expanding placeholders of {file} configuration: found item "{item}" in object dictionary that isn\'t a string!'.format(
                        file=self.config_name, item=item
                    )
                )

    ############################################################################
    def writeJSON(self, json_path: FilePath, to_ignore: List[str] = []) -> None:
        """Writes the class instance to the JSON file.

        Args:
            json_path (FilePath): The path to the file to write the JSON to
            to_ignore (List[str]): The list of attributes to ignore
        """
        self.json_path = json_path
        writeJSON(
            getJSONDict(self, to_ignore),
            json_path=json_path,
            file_text=self.config_name,
            conf_file_name=self.file_name,
        )

    ###########################################################################
    def hasConfigChangedOnDisk(self) -> bool:
        """Returns `True` if the JSON file has been changed since the time the
        checksum has been calculated.

        Returns:
            bool: `True` if the original JSON file has changed since the time
                    the file's checksum has been saved.
                   `False` else
        """
        try:
            return self.orig_file.hasChanged(not_exist_is_excp=True)
        except Exception as excp:
            self._logger.error(
                'error "{error}" calculating checksum of JSON file "{path}"'.format(
                    error=excp, path=self.orig_file.path
                )
            )
            return True

    ###########################################################################
    def reReadIfChangedOnDisk(self) -> None:
        """Checks if the JSON configuration file has been changed since the
        time the checksum has been calculated, if yes, it is reread from disk.
        """
        try:
            if self.orig_file.hasChanged(not_exist_is_excp=True):
                self._logger.warning(
                    'Rereading {name} configuration from JSON file "{json_path}"'.format(
                        name=self.config_name, json_path=self.orig_file.path
                    )
                )
                tmp_json_path = self.json_path
                self.readJSON(json_path=self.orig_file.path)
                self.json_path = tmp_json_path

        except Exception as excp:
            self._logger.error(
                'error "{error}" checking whether to reread JSON file "{path}"'.format(
                    error=excp, path=self.orig_file.path
                )
            )

    ###########################################################################
    def reWriteIfChangedOnDisk(self) -> None:
        """Checks if the JSON configuration file has been changed since the
        time the checksum has been calculated, if yes, it is reread from disk
        and the generated JSON file is written to it's file path.
        """
        try:
            if self.orig_file.hasChanged(not_exist_is_excp=True):
                tmp_json_path = self.json_path
                self.readJSON(json_path=self.orig_file.path)
                self.json_path = tmp_json_path
                self.writeJSON(json_path=self.json_path)

        except Exception as excp:
            self._logger.error(
                'error "{error}" checking whether to rewrite JSON file "{path}"'.format(
                    error=excp, path=self.orig_file.path
                )
            )

    ##########################################################################
    def addAttributesIfNotExist(self, attributes: Dict[str, object]) -> None:
        """Adds each attribute in the given dictionary of attributes.

        The key of the dictionary is the attribute's name, the value the
        deault value to set the attribute to, if it didn't exist.

        Args:
            attributes (Dict[str, object]): The dictionary of attributes and
                                            default values
        """
        for attribute in attributes:
            if not hasattr(self, attribute):
                setattr(self, attribute, attributes[attribute])

    ###########################################################################

    def __repr__(self) -> str:
        """Returns a string representing the JSON object.

        Returns:
            str: A strings representation of the object's data
        """
        return "{name}:\n{config}".format(
            name=self.config_name,
            config=pprint.pformat(getJSONDict(self), indent=4, sort_dicts=False),
        )
