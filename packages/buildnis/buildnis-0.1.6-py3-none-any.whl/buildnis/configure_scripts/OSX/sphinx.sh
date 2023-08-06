#!/bin/bash
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     sphinx.sh
# Date:     22.Feb.2021
################################################################################

# Sphinx, install with
# pip install sphinx

# assumes sphinx-build is in the PATH
SPHINX_VERSION=$(sphinx-build --version |head -1)
SPHINX_PATH=$(dirname `which sphinx-build`)

echo "{"
echo '    "build_tools":'
echo "    ["
echo "         {"
echo "            \"name\": \"Sphinx\","
echo "            \"name_long\": \"${SPHINX_VERSION}\","
echo "            \"version\": \"\","
echo "            \"version_arg\": \"--version\","
echo "            \"version_regex\": \"^\\\\S+ (.*)\","
echo "            \"build_tool_exe\": \"sphinx-build\","
echo "            \"install_path\": \"${SPHINX_PATH}\","
echo "            \"env_script\": \"\""
echo "         }"
echo "    ]"
echo "}"