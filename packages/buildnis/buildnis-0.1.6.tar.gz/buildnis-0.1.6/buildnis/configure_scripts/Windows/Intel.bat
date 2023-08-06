:: SPDX-License-Identifier: MIT
:: Copyright (C) 2021 Roland Csaszar
::
:: Project:  Buildnis
:: File:     Intel.bat
:: Date:     15.Feb.2021
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: searches for the Intel compilers setting batch file.

@echo off

:: ONEAPI_ROOT
:: C:\Program Files (x86)\Intel\oneAPI\

:: Intel needs intel64 or ia32 as arguments to set 64 or 32 bit compilers
set X64_ARGUMENT=intel64
set I86_ARGUMENT=ia32

:: parse command line arguments
:PARSE_ARGS
if /i "%1"==""    goto :END_PARSE_ARGS
if /i "%1"=="x64" (set CMD_ARG=%X64_ARGUMENT%) & shift & goto :PARSE_ARGS
if /i "%1"=="x86" (set CMD_ARG=%I86_ARGUMENT%) & shift & goto :PARSE_ARGS
:END_PARSE_ARGS

set ICL_VERSION=
set ICX_VERSION=
set IFORT_VERSION=
set IFX_VERSION=
set PYTHON_VERSION=
set ENV_SCRIPT=


:: search for the environment script setvars.bat
if exist "%ONEAPI_ROOT%setvars.bat" (
    set ENV_SCRIPT="%ONEAPI_ROOT%setvars.bat"
    goto :HAVE_ENV_SCRIPT
) else if exist "%ProgramFiles(x86)%\Intel\oneAPI\setvars.bat" (
    set ENV_SCRIPT="%ProgramFiles(x86)%\Intel\oneAPI\setvars.bat"
    goto :HAVE_ENV_SCRIPT
)

set ENV_SCRIPT=""

:HAVE_ENV_SCRIPT

call %ENV_SCRIPT% %CMD_ARG% > nul 2>&1

SetLocal EnableDelayedExpansion

for /f "delims=" %%l in ('icl /QV 2^>^&1') do (    
    if /i "!ICL_VERSION!"=="" (        
        set ICL_VERSION=%%l
        call :TRIM ICL_VERSION
    )
)

for /f "delims=" %%l in ('icx /QV 2^>^&1') do (    
    if /i "!ICX_VERSION!"=="" (       
        set ICX_VERSION=%%l
        call :TRIM ICX_VERSION
    )
)

for /f "delims=" %%l in ('ifort /QV 2^>^&1') do (    
    if /i "!IFORT_VERSION!"=="" (        
        set IFORT_VERSION=%%l
        call :TRIM IFORT_VERSION
    )
)

for /f "delims=" %%l in ('ifx /QV 2^>^&1') do (    
    if /i "!IFX_VERSION!"=="" (        
        set IFX_VERSION=%%l
        call :TRIM IFX_VERSION
    )
)

for /f "delims=" %%l in ('python --version') do (    
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
echo         "name": "Intel C++ Classic",
echo         "name_long": "%ICL_VERSION%",
echo         "version": "",
echo         "version_arg": "/QV",
echo         "version_regex": ", Version (.*) Build",
echo         "build_tool_exe": "icl",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%,
echo         "env_script_arg": "%CMD_ARG%"
echo     },
echo     {
echo         "name": "Intel DPC++/C++",
echo         "name_long": "%ICX_VERSION%",
echo         "version": "",
echo         "version_arg": "/QV",
echo         "version_regex": ", Version (.*) Build",
echo         "build_tool_exe": "icx",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%,
echo         "env_script_arg": "%CMD_ARG%"
echo     },
echo     {
echo         "name": "Intel Fortran Classic",
echo         "name_long": "%IFORT_VERSION%",
echo         "version": "",
echo         "version_arg": "/QV",
echo         "version_regex": ", Version (.*) Build",
echo         "build_tool_exe": "ifort",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%,
echo         "env_script_arg": "%CMD_ARG%"
echo     },
echo     {
echo         "name": "Intel Fortran (ifx)",
echo         "name_long": "%IFX_VERSION%",
echo         "version": "",
echo         "version_arg": "/QV",
echo         "version_regex": ", Version (.*) Build",
echo         "build_tool_exe": "ifx",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%,
echo         "env_script_arg": "%CMD_ARG%"
echo     },
echo     {
echo         "name": "Intel Python",
echo         "name_long": "%PYTHON_VERSION%",
echo         "version": "",
echo         "version_arg": "--version",
echo         "version_regex": "Python (.*) ::",
echo         "build_tool_exe": "python",
echo         "install_path": "",
echo         "env_script": %ENV_SCRIPT:\=\\%
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

