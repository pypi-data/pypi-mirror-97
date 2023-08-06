#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     clang.sh
# Date:     22.Feb.2021
################################################################################


# clang comes with XCode. 
# https://developer.apple.com/xcode/resources/

# assumes clang is in the PATH
CLANG_VERSION=$(clang --version |head -1|cut -d'(' -f1)
CLANG_PATH=$(dirname `which clang`)
CLANGPP_VERSION=$(clang++ --version |head -1|cut -d'(' -f1)
CLANGPP_PATH=$(dirname `which clang++`)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"Clang\","
echo "            \"name_long\": \"${CLANG_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"clang\","
echo "            \"install_path\": \"${CLANG_PATH}\","
echo "            \"env_script\": \"\""
echo "         },"
echo "         {"
echo "            \"name\": \"Clang++\","
echo "            \"name_long\": \"${CLANGPP_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"clang++\","
echo "            \"install_path\": \"${CLANGPP_PATH}\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"