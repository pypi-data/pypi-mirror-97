#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     JavaVM.sh
# Date:     22.Feb.2021
################################################################################

# assumes Java is in the PATH
JAVA_VERSION=$(java --version|head -2 |tail -1)
JAVA_PATH=$(dirname `which java`)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"Java\","
echo "            \"name_long\": \"${JAVA_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"^\\\\S+ (\\\\S+) \","
echo "            \"build_tool_exe\": \"java\","
echo "            \"install_path\": \"${JAVA_PATH}\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"