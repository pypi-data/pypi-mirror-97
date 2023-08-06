:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     pythonInt.bat
:: Date:     16.Feb.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: check if Python is in the path

@echo off

SetLocal EnableDelayedExpansion

set PYTHON_VERSION=

for /f "delims=" %%l in ('python -V') do (
    if /i "!PYTHON_VERSION!"=="" (
        set PYTHON_VERSION=%%l
        call :TRIM PYTHON_VERSION
    )
)

:: JSON output
echo {
echo "build_tools": 
echo [
echo     {
echo         "name": "Python",
echo         "name_long": "%PYTHON_VERSION%",
echo         "version": "",
echo         "version_arg": "--version",
echo         "version_regex": "^\\S+ (.*)",
echo         "build_tool_exe": "python",
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
