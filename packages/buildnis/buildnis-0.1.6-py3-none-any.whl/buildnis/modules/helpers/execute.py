# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     execute.py
# Date:     21.Feb.2021
###############################################################################

from __future__ import annotations
import re
from typing import List
import subprocess

from buildnis.modules.config import CmdOutput, FilePath


class ExecuteException(Exception):
    """The Exception is thrown if the execution of the given commandline fails."""

    pass


################################################################################
def runCommand(
    exe: FilePath,
    args: List[str] = [],
    env_script: FilePath = "",
    env_script_args: List[str] = [],
    source_env_script: bool = False,
) -> CmdOutput:
    """Executes the given command with the given arguments.

    The argument `exe` is the executable's name or path, needed arguments can be
    passed in the list `args`.
    In `env_script` the command to set up an environment can be given, with
    needed arguments to this environment script in the list `env_script_args`.

    Args:
        exe (FilePath): The name of the executable or path to the executable
                        to call
        args (List[str], optional): The list of arguments to pass to the executable.
                                    Defaults to [].
        env_script (FilePath, optional): The environment script to set up the
                    environment prior to calling the executable. Defaults to "".
        env_script_args (List[str], optional): List of arguments to pass to the
                environment script `env_script` Defaults to [].
        source_env_script (bool): Call the environment script (`False`) or source
                    the environment script (set this to `True`)

    Raises:
        ExecuteException: if something goes wrong

    Returns:
        CmdOutput: The output of the executed command as tuple (stdout, stderr)
    """
    cmd_line_args = []

    # TODO really always call bash?
    if env_script != "":
        if source_env_script == True:
            cmd_line_args.append("bash")
            cmd_line_args.append("-c")
            source_cmd = "source " + env_script + " " + " ".join(env_script_args)
            source_cmd = source_cmd + " && " + exe
            source_cmd = source_cmd + " " + " ".join(args)
            cmd_line_args.append(source_cmd)
        else:
            cmd_line_args.append(env_script)
            for env_arg in env_script_args:
                cmd_line_args.append(env_arg)
            cmd_line_args.append("&&")

    if env_script == "" or not source_env_script:
        cmd_line_args.append(exe)

        for arg in args:
            if arg != "":
                cmd_line_args.append(arg)

    try:
        process_result = subprocess.run(
            args=cmd_line_args, capture_output=True, text=True, check=False, timeout=120
        )
    except Exception as excp:
        raise ExecuteException(excp)

    return CmdOutput(std_out=process_result.stdout, err_out=process_result.stderr)


################################################################################
def doesExecutableWork(
    exe: FilePath,
    check_regex: str,
    regex_group: int = 0,
    args: List[str] = [],
    env_script: FilePath = "",
    env_script_args: List[str] = [],
    source_env_script: bool = False,
) -> str:
    """Checks if the given command line works.

    Tries to run the command with the given arguments (see `runCommand`) and
    parses the output of the program, tries to match the given regex `check_regex`
    in the output (`stdout` and `stderr`) of the command. If the match group
    `regex_group` (defaults to 0, the whole regex) is found in the output, the
    function returns the matched string.

    Args:
        exe (FilePath): The name of the executable or path to the executable
                        to call
        check_regex (str): The regex to parse the output of the program with.
                    Both `stdout` and `stderr` are parsed, `stderr` only if
                    `stdout` doesn't match
        regex_group (int): the index of the match group to check.
                        Defaults to 0, the whole regex.
        args (List[str], optional):  The list of arguments to pass to the executable.
                                    Defaults to [].
        env_script (FilePath, optional): The environment script to set up the
                    environment prior to calling the executable. Defaults to "".
        env_script_args (List[str], optional): List of arguments to pass to the
                environment script `env_script` Defaults to [].
        source_env_script (bool): Call the environment script (`False`) or source
                    the environment script (set this to `True`)

    Raises:
        ExecuteException: if something goes wrong

    Returns:
        str: the matched string if the regex matches the output, the empty string
             '' otherwise.
    """
    ret_val = ""

    try:
        output = runCommand(
            exe=exe,
            args=args,
            env_script=env_script,
            env_script_args=env_script_args,
            source_env_script=source_env_script,
        )

        run_regex = re.search(check_regex, output.std_out)
        if run_regex != None and run_regex.group(regex_group):
            ret_val = run_regex.group(regex_group)

        else:
            run_regex = re.search(check_regex, output.err_out)
            if run_regex != None and run_regex.group(regex_group):
                ret_val = run_regex.group(regex_group).strip()

    except Exception as excp:
        raise ExecuteException(excp)

    return ret_val
