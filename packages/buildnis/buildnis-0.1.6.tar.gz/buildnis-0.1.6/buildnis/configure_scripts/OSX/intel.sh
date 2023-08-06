#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     clang.sh
# Date:     24.Feb.2021
################################################################################

# Intel OneAPI C++ and Fortran compilers and a Python implementation.
# Download at 
# https://software.intel.com/content/www/us/en/develop/tools/oneapi/base-toolkit/download.html
# and
# https://software.intel.com/content/www/us/en/develop/tools/oneapi/hpc-toolkit.html

# search for the intel environment setter ...
INTEL_ENV_SCRIPT=$(find /opt/intel/oneapi -name "setvar*" -type f|sort -r|head -1)

source ${INTEL_ENV_SCRIPT} > /dev/null

ICC_LONG_NAME=$(icc --version|head -1)
IFORT_LONG_NAME=$(ifort --version|head -1)
INTEL_PYTHON_NAME=$(python --version|head -1)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"Intel C++\","
echo "            \"name_long\": \"${ICC_LONG_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"\\\\(ICC\\\\) (\\\\S*) \","
echo "            \"build_tool_exe\": \"icc\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"${INTEL_ENV_SCRIPT}\""
echo "         },"
echo "         {"
echo "            \"name\": \"Intel Fortran\","
echo "            \"name_long\": \"${IFORT_LONG_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"\\\\(IFORT\\\\) (\\\\S*) \","
echo "            \"build_tool_exe\": \"ifort\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"${INTEL_ENV_SCRIPT}\""
echo "         }",
echo "         {"
echo "            \"name\": \"Intel Python\","
echo "            \"name_long\": \"${INTEL_PYTHON_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"Python (\\\\S+) \","
echo "            \"build_tool_exe\": \"python\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"${INTEL_ENV_SCRIPT}\""
echo "         }"
echo "    ]"
echo "}"