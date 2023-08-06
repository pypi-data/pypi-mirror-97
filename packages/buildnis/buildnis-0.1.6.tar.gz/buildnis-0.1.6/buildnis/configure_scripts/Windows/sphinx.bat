:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     sphinx.bat
:: Date:     16.Feb.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


@echo off

SetLocal EnableDelayedExpansion

:: check if Sphinx is in the PATH

set SPHINX_VERSION=

for /f "delims=" %%l in ('sphinx-build  --version') do (
    if /i "!SPHINX_VERSION!"=="" (
        set SPHINX_VERSION=%%l
        call :TRIM SPHINX_VERSION
    )
)

:: JSON output
echo {
echo "build_tools": 
echo [
echo     {
echo         "name": "Sphinx",
echo         "name_long": "%SPHINX_VERSION%",
echo         "version": "",
echo         "version_arg": "--version",
echo         "version_regex": "^\\S+ (.*)",
echo         "build_tool_exe": "sphinx-build",
echo         "install_path": "",
echo         "env_script": ""
echo     }
echo ]
echo }


EndLocal

GOTO :EOF


:: trim spaces off the strings
:TRIM
SetLocal EnableDelayedExpansion
Call :TRIMHELPER %%%1%%
EndLocal & set %1=%helper_tmp%
GOTO :EOF

:TRIMHELPER
set helper_tmp=%*
GOTO :EOF
