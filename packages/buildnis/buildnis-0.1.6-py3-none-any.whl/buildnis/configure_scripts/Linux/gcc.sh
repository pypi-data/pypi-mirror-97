#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     gcc.sh
# Date:     25.Feb.2021
################################################################################

GCC_VERSION=$(gcc -v 2>&1|tail -1|sed 's/ (GCC) //'|sed 's/ \[revision.*//')

GPP_VERSION=$(g++ -v 2>&1|tail -1|sed 's/ (GCC) //'|sed 's/ \[revision.*//')

GFORTRAN_VERSION=$(gfortran -v 2>&1|tail -1|sed 's/ (GCC) //'|sed 's/ \[revision.*//')

# RedHat has a special environment to set for newer GCC: scl - doesn't work ...

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"GCC\","
echo "            \"name_long\": \"${GCC_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"-v\","
echo "            \"version_regex\": \"version ([^\\\\[(\\\\n]+)\","
echo "            \"build_tool_exe\": \"gcc\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         },"
echo "         {"
echo "            \"name\": \"GCC G++\","
echo "            \"name_long\": \"${GPP_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"-v\","
echo "            \"version_regex\": \"version ([^\\\\[(\\\\n]+)\","
echo "            \"build_tool_exe\": \"g++\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }",
echo "         {"
echo "            \"name\": \"GFortran\","
echo "            \"name_long\": \"${GFORTRAN_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"-v\","
echo "            \"version_regex\": \"version ([^\\\\[(\\\\n]+)\","
echo "            \"build_tool_exe\": \"gfortran\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"

