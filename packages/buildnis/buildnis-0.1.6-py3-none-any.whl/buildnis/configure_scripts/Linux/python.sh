#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     python.sh
# Date:     24.Feb.2021
################################################################################

# offical, user friendly name of the executable
NAME="Python"

# name to call the executable with
EXE_NAME="python3"

# argument to get the program's version
VERSION_ARG="--version"

# assumes PROGRAM is in the PATH
PROGRAM_VERSION=$(${EXE_NAME} ${VERSION_ARG} 2>&1)
PROGRAM_PATH=$(dirname `which ${EXE_NAME}`)

# WARNING: this is a JSON encoded regex to use with Python, not to parse the
# version output now
VERSION_REGEX_PYTHON="^\\\\S+ (.*)"

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"${NAME}\","
echo "            \"name_long\": \"${PROGRAM_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"${VERSION_ARG}\","
echo "            \"version_regex\": \"${VERSION_REGEX_PYTHON}\","
echo "            \"build_tool_exe\": \"${EXE_NAME}\","
echo "            \"install_path\": \"${PROGRAM_PATH}\","
echo "            \"env_script\": \"${ENV_SCRIPT_PATH}\""
echo "         }"
echo "    ]"
echo "}"