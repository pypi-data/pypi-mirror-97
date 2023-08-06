:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     Java.bat
:: Date:     16.Feb.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
@echo off

setlocal enabledelayedexpansion

:: check, if java is in the PATH
set JAVA_VERSION=
set JAVA_PATH=
for /f "delims=" %%l in ('java --version') do (
    if /i "!JAVA_VERSION!"=="" (
        set JAVA_VERSION=%%l
        call :TRIM JAVA_VERSION
    )
)

:: check JAVA_HOME, if not in PATH
if /i "!JAVA_VERSION!"=="" (    
    if exist "%JAVA_HOME%\bin\java.exe" (       
        for /f "delims=" %%l in ('"%JAVA_HOME%\bin\java.exe" --version') do (           
            if /i "!JAVA_VERSION!"=="" (
                set JAVA_VERSION=%%l
                set JAVA_PATH="%JAVA_HOME%\bin\"
                call :TRIM JAVA_VERSION
            )
        )
    )
)

if /i "%JAVA_PATH%"=="" set JAVA_PATH=""

:: JSON output
echo {
echo "build_tools": 
echo [
echo     {
echo         "name": "Java",
echo         "name_long": "%JAVA_VERSION%",
echo         "version": "",
echo         "version_arg": "--version",
echo         "version_regex": "^\\S+ (\\S+) ",
echo         "build_tool_exe": "java",
echo         "install_path": %JAVA_PATH%,
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