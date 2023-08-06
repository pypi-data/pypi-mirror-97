#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     clang.sh
# Date:     25.Feb.2021
################################################################################

# flang --version
# f18 compiler (under development), version 11.1.0

CLANG_VERSION=$(clang --version 2>&1|sed '/^$/d'|head -1)
CLANGPP_VERSION=$(clang++ --version 2>&1|sed '/^$/d'|head -1)
FLANG_VERSION=$(flang --version 2>&1|sed '/^$/d'|head -1)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"Clang\","
echo "            \"name_long\": \"${CLANG_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version ([^(\\\\n]+)\","
echo "            \"build_tool_exe\": \"clang\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         },"
echo "         {"
echo "            \"name\": \"Clang++\","
echo "            \"name_long\": \"${CLANGPP_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version ([^(\\\\n]+)\","
echo "            \"build_tool_exe\": \"clang++\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }",
echo "         {"
echo "            \"name\": \"FLang\","
echo "            \"name_long\": \"${FLANG_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \", version ([^(\\\\n]+)\","
echo "            \"build_tool_exe\": \"flang\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"



