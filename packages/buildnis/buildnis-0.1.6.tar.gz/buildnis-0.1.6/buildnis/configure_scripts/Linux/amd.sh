#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     amd.sh
# Date:     25.Feb.2021
################################################################################


#/opt/AMD/aocc-compiler-2.3.0/setenv_AOCC.sh 
ENV_SCRIPT=$(find /opt/AMD/aocc-* -name "setenv*")

source ${ENV_SCRIPT} >/dev/null 2>&1

CLANG_VERSION=$(clang --version|head -1|sed 's/ (based.*)//')
CLANGPP_VERSION=$(clang++ --version|head -1|sed 's/ (based.*)//')
FLANG_VERSION=$(flang --version|head -1|sed 's/ (based.*)//')



# clang  --version
# #AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10) (based on LLVM Mirror.Version.11.0.0)
# clang  --version| grep "^.* (CL"

# clang++ --version
# AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10) (based on LLVM Mirror.Version.11.0.0

# flang --version
# AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"AMD AOCC C\","
echo "            \"name_long\": \"${CLANG_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"clang\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"${ENV_SCRIPT}\""
echo "         },"
echo "         {"
echo "            \"name\": \"AMD AOCC C++\","
echo "            \"name_long\": \"${CLANGPP_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"clang++\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"${ENV_SCRIPT}\""
echo "         }",
echo "         {"
echo "            \"name\": \"AMD AOCC Fortran\","
echo "            \"name_long\": \"${FLANG_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"version (.*) \\\\(\","
echo "            \"build_tool_exe\": \"flang\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"${ENV_SCRIPT}\""
echo "         }"
echo "    ]"
echo "}"