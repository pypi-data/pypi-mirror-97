# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     config_parser.py
# Date:     28.Feb.2021
###############################################################################

from __future__ import annotations

import re
import logging
import datetime
from typing import List

from buildnis.modules.helpers.files import FileCompare
from buildnis.modules.config import (
    LINUX_OS_STRING,
    OSX_OS_STRING,
    WINDOWS_OS_STRING,
    config_values,
)

# regexes to use

project_root_regex = re.compile("\$\{(PROJECT_ROOT)\}")
"""Regex to find the placeholder `${PROJECT_ROOT}`.
"""

project_name_regex = re.compile("\$\{(PROJECT_NAME)\}")
"""Regex to find the placeholder `${PROJECT_NAME}`.
"""

project_version_regex = re.compile("\$\{(PROJECT_VERSION)\}")
"""Regex to find the placeholder `${PROJECT_VERSION}`.
"""

project_author_regex = re.compile("\$\{(PROJECT_AUTHOR)\}")
"""Regex to find the placeholder `${PROJECT_AUTHOR}`.
"""

project_company_regex = re.compile("\$\{(PROJECT_COMPANY)\}")
"""Regex to find the placeholder `${PROJECT_COMPANY}`.
"""

project_copyright_info_regex = re.compile("\$\{(PROJECT_COPYRIGHT_INFO)\}")
"""Regex to find the placeholder `${PROJECT_COPYRIGHT_INFO}`.
"""

project_web_url_regex = re.compile("\$\{(PROJECT_WEB_URL)\}")
"""Regex to find the placeholder `${PROJECT_WEB_URL}`.
"""

project_email_regex = re.compile("\$\{(PROJECT_EMAIL)\}")
"""Regex to find the placeholder `${PROJECT_EMAIL}`.
"""

project_cfg_dir_regex = re.compile("\$\{(PROJECT_CONFIG_DIR_PATH)\}")
"""Regex to find the placeholder `${PROJECT_CONFIG_DIR_PATH}`.
"""

host_os_regex = re.compile("\$\{(HOST_OS)\}")
"""Regex to find the placeholder `${HOST_OS}`.
"""

host_name_regex = re.compile("\$\{(HOST_NAME)\}")
"""Regex to find the placeholder `${HOST_NAME}`.
"""

host_cpu_arch_regex = re.compile("\$\{(HOST_CPU_ARCH)\}")
"""Regex to find the placeholder `${HOST_CPU_ARCH}`.
"""

host_num_cores_regex = re.compile("\$\{(HOST_NUM_CORES)\}")
"""Regex to find the placeholder `${HOST_NUM_CORES}`.
"""

host_num_log_cores_regex = re.compile("\$\{(HOST_NUM_LOG_CORES)\}")
"""Regex to find the placeholder `${HOST_NUM_LOG_CORES}`.
"""

os_name_windows_regex = re.compile("\$\{(OS_NAME_WINDOWS)\}")
"""Regex to find the placeholder `${OS_NAME_WINDOWS}`.
"""

os_name_linux_regex = re.compile("\$\{(OS_NAME_LINUX)\}")
"""Regex to find the placeholder `${OS_NAME_LINUX}`.
"""

os_name_osx_regex = re.compile("\$\{(OS_NAME_OSX)\}")
"""Regex to find the placeholder `${OS_NAME_OSX}`.
"""

current_time_regex = re.compile("\$\{(TIME)\}")
"""Regex to find the placeholder `${TIME}`.
"""

current_date_regex = re.compile("\$\{(DATE)\}")
"""Regex to find the placeholder `${DATE}`.
"""

current_year_regex = re.compile("\$\{(YEAR)}")
"""Regex to find the placeholder `${YEAR}`.
"""

current_month_regex = re.compile("\$\{(MONTH)}")
"""Regex to find the placeholder `${MONTH}`.
"""

current_day_regex = re.compile("\$\{(DAY)}")
"""Regex to find the placeholder `${DAY}`.
"""

placeholder_regex = re.compile("\$\{(.*)\}")
"""Regex to find general placefolders, of the form `${STRING}`, where string
is to be substituted for a value of another configuration item.
"""


############################################################################
def replaceConstants(item2: str) -> str:
    """Replaces all known constants defined in `config_values.py` in the given string.

    These are placeholders like `${PROJECT_ROOT}`, `${PROJECT_NAME}`, ...

    Args:
        item (str): The string to parse for known constants.

    Returns:
        str: The substitution if a placeholder has been found, the unaltered
                string else.
    """
    ret_val = item2

    result = project_root_regex.search(ret_val)
    if result:
        ret_val = project_root_regex.sub(
            config_values.PROJECT_ROOT.replace("\\", "\\\\"), ret_val
        )
        
    result = project_name_regex.search(ret_val)
    if result:
        ret_val = project_name_regex.sub(
            config_values.PROJECT_NAME.replace("\\", "\\\\"), ret_val
        )

    result = project_version_regex.search(ret_val)
    if result:
        ret_val = project_version_regex.sub(
            config_values.PROJECT_VERSION.replace("\\", "\\\\"), ret_val
        )       

    result = project_author_regex.search(ret_val)
    if result:
        ret_val = project_author_regex.sub(
            config_values.PROJECT_AUTHOR.replace("\\", "\\\\"), ret_val
        )        

    result = project_company_regex.search(ret_val)
    if result:
        ret_val = project_company_regex.sub(
            config_values.PROJECT_COMPANY.replace("\\", "\\\\"), ret_val
        )        

    result = project_copyright_info_regex.search(ret_val)
    if result:
        ret_val = project_copyright_info_regex.sub(
            config_values.PROJECT_COPYRIGHT_INFO.replace("\\", "\\\\"), ret_val
        )       

    result = project_web_url_regex.search(ret_val)
    if result:
        ret_val = project_web_url_regex.sub(
            config_values.PROJECT_WEB_URL.replace("\\", "\\\\"), ret_val
        )      

    result = project_email_regex.search(ret_val)
    if result:
        ret_val = project_email_regex.sub(
            config_values.PROJECT_EMAIL.replace("\\", "\\\\"), ret_val
        )       

    result = project_cfg_dir_regex.search(ret_val)
    if result:
        ret_val = project_cfg_dir_regex.sub(
            config_values.PROJECT_CONFIG_DIR_PATH.replace("\\", "\\\\"), ret_val
        )

    result = host_os_regex.search(ret_val)
    if result:
        ret_val = host_os_regex.sub(config_values.HOST_OS.replace("\\", "\\\\"), ret_val)
       
    result = host_name_regex.search(ret_val)
    if result:
        ret_val = host_name_regex.sub(
            config_values.HOST_NAME.replace("\\", "\\\\"), ret_val
        )       

    result = host_cpu_arch_regex.search(ret_val)
    if result:
        ret_val = host_cpu_arch_regex.sub(
            config_values.HOST_CPU_ARCH.replace("\\", "\\\\"), ret_val
        )       

    result = host_num_cores_regex.search(ret_val)
    if result:
        ret_val = host_num_cores_regex.sub(
            config_values.HOST_NUM_CORES.replace("\\", "\\\\"), ret_val
        )

    result = host_num_log_cores_regex.search(ret_val)
    if result:
        ret_val = host_num_log_cores_regex.sub(
            config_values.HOST_NUM_LOG_CORES.replace("\\", "\\\\"), ret_val
        )      

    result = os_name_osx_regex.search(ret_val)
    if result:
        ret_val = os_name_osx_regex.sub(OSX_OS_STRING, ret_val)

    result = os_name_linux_regex.search(ret_val)
    if result:
        ret_val = os_name_linux_regex.sub(LINUX_OS_STRING, ret_val)       

    result = os_name_windows_regex.search(ret_val)
    if result:
        ret_val = os_name_windows_regex.sub(WINDOWS_OS_STRING, ret_val)

    result = current_date_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_date_regex.sub(now_date.strftime("%d.%m.%Y"), ret_val)
      
    result = current_year_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_year_regex.sub(now_date.strftime("%Y"), ret_val)      

    result = current_month_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_month_regex.sub(now_date.strftime("%m"), ret_val)
     
    result = current_day_regex.search(ret_val)
    if result:
        now_date = datetime.now()
        ret_val = current_day_regex.sub(now_date.strftime("%d"), ret_val)
     

    result = current_time_regex.search(ret_val)
    if result:
        now_time = datetime.now()
        ret_val = current_time_regex.sub(now_time.strftime("%H:%M:%S"), ret_val)   

    return ret_val


############################################################################
def expandItem(item: str, parents: List[object]) -> object:
    """Parses the given item, if it contains a placeholder, that placeholder
    is expanded. If the item doesn't contain a placeholder, the item's
    unaltered string is returned.

    Args:
        item (str): The item to parse and expand its placeholder
        parents (List[object]): The parents of the item to search for
                                the placeholder's content.

    Returns:
        object: The expanded string if the item contained a placeholder, the
             original string else. If the placeholder points to another
             object that is not a string, this object is returned.
    """
    ret_val = replaceConstants(item)

    result = placeholder_regex.search(ret_val)
    parent_to_use_id = 0
    if result:
        # print("Found Placeholder: {place}".format(place=result.group(1)))
        placeholder = result.group(1)
        parent_regex = re.compile("(\.\./)")

        result = parent_regex.match(placeholder)
        while result != None:
            placeholder = placeholder.removeprefix("../")
            result = parent_regex.match(placeholder)
            parent_to_use_id -= 1

        try:
            parent = parents[parent_to_use_id]

            if isinstance(parent[placeholder], str):
                substitute = parent[placeholder].replace("\\", "\\\\")
            else:
                substitute = parent[placeholder]
            # print("Replace {ph} with: {elem}".format(ph=placeholder, elem=substitute))
        except:
            try:
                parent = parents[parent_to_use_id]
                if isinstance(getattr(parent, placeholder), str):
                    substitute = getattr(parent, placeholder).replace("\\", "\\\\")
                else:
                    substitute = getattr(parent, placeholder)
                # print(
                #     "Replace {ph} with: {elem}, class".format(
                #         ph=placeholder, elem=substitute
                #     )
                # )
            except:
                return ret_val

        if isinstance(substitute, str):
            ret_val = placeholder_regex.sub(substitute, item)
        else:
            ret_val = substitute

    return ret_val


###############################################################################
def parseConfigElement(element: object, parents: List[object] = []) -> object:
    """Parses the given config element and replaces placeholders.
    Placeholders are strings of the form `${PLACEHOLDER}`, with start with a
    dollar sign followed by an opening curly brace and end with a curly brace.
    The string between the two curly braces is changed against it's value.

    Args:
        element (object): The configuration element to parse and expand.
        parent (List[object], optional): The parent and the parent's parent and it's
        parent as a list, starting with the parent as first element. Defaults to None.

    Returns:

        object: The parsed and expanded object.
    """
    # print("parseConfigElement: {element}, parents: {parents}".format(
    #    element=element.__class__, parents=len(parents)))
    local_parents = parents.copy()
    if isinstance(element, list):
        tmp_list = []
        for subitem in element:

            if hasattr(subitem, "__dict__"):
                tmp_list.append(parseConfigElement(subitem, local_parents))

            elif isinstance(subitem, dict):
                local_parents.append(element)
                for key in subitem:
                    subitem[key] = parseConfigElement(subitem[key], local_parents)

                tmp_list.append(subitem)
            else:
                if isinstance(subitem, str):
                    tmp_list.append(expandItem(subitem, local_parents))
                else:
                    tmp_list.append(subitem)
        return tmp_list

    elif isinstance(element, FileCompare):
        return element

    elif isinstance(element, logging.Logger):
        return element

    elif isinstance(element, str):
        return expandItem(element, local_parents)

    elif hasattr(element, "__dict__"):
        local_parents = parents.copy()
        local_parents.append(element)
        for key in element.__dict__:
            element.__dict__[key] = parseConfigElement(
                element.__dict__[key], local_parents
            )
        return element

    else:
        return element
