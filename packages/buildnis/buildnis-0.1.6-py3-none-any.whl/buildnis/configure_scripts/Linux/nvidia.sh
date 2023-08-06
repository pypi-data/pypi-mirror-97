#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     nvidia.sh
# Date:     24.Feb.2021
################################################################################

NVC_LONG_NAME=$(nvc --version|head -2|tail -1)
NVCPP_LONG_NAME=$(nvc++ --version|head -2|tail -1)
NFORT_LONG_NAME=$(nvfortran --version|head -2|tail -1)
NVCC_LONG_NAME=$(nvcc --version|head -4|tail -1)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"NVidia C++\","
echo "            \"name_long\": \"${NVC_LONG_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"nv\\\\S+ (\\\\S*)\","
echo "            \"build_tool_exe\": \"nvc\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         },"
echo "         {"
echo "            \"name\": \"NVidia C++\","
echo "            \"name_long\": \"${NVCPP_LONG_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"nv\\\\S+ (\\\\S*)\","
echo "            \"build_tool_exe\": \"nvc++\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }",
echo "         {"
echo "            \"name\": \"NVidia Fortran\","
echo "            \"name_long\": \"${NFORT_LONG_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"nv\\\\S+ (\\\\S*)\","
echo "            \"build_tool_exe\": \"nvfortran\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }",
echo "         {"
echo "            \"name\": \"NVidia CUDA\","
echo "            \"name_long\": \"${NVCC_LONG_NAME}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \", release \\\\S+ (\\\\S+)\","
echo "            \"build_tool_exe\": \"nvcc\","
echo "            \"install_path\": \"\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"
