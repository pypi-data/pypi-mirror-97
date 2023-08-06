#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     pythonint.sh
# Date:     22.Feb.2021
################################################################################

# You get the latest PYthon versions at
# https://www.python.org/downloads/

# assumes python is in the PATH
PYTHON_VERSION=$(python3 --version 2>&1)
PYTHON_PATH=$(dirname `which python3`)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"Python\","
echo "            \"name_long\": \"${PYTHON_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"^\\\\S+ (.*)\","
echo "            \"build_tool_exe\": \"python3\","
echo "            \"install_path\": \"${PYTHON_PATH}\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"