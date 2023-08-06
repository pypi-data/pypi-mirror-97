#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

from __future__ import annotations
from buildnis.modules.config import CFG_DIR_NAME
from buildnis.modules import EXT_ERR_IMP_MOD

try:
    import sys
    import os
    import pprint
    import logging
    import pathlib
    from typing import List, Tuple
except ImportError as exp:
    print('ERROR: error "{error}" importing modules'.format(error=exp), file=sys.stderr)
    sys.exit(EXT_ERR_IMP_MOD)

try:
    from buildnis.modules.config.config_dir_json import ConfigDirJson
    from buildnis.modules.config import config_values
    from buildnis.modules.config import config
    from buildnis.modules.helpers.files import checkIfIsFile
    from buildnis.modules.config import PROJECT_FILE_NAME
    from buildnis.modules.helpers.logging import getProgramLogger
    from buildnis.modules.config import project_dependency
    from buildnis.modules.helpers.commandline import parseCommandLine
    from buildnis.modules.config import check
    from buildnis.modules.config.host import Host
    from buildnis.modules.config import FilePath, PROJECT_DEP_FILE_NAME
    from buildnis.modules import EXT_OK
    from buildnis.modules.config import HOST_FILE_NAME
    from buildnis.modules.config import BUILD_TOOL_CONFIG_NAME
except ImportError as exp:
    print(
        'ERROR: error "{error}" importing own modules'.format(error=exp),
        file=sys.stderr,
    )
    sys.exit(EXT_ERR_IMP_MOD)


################################################################################
def main():
    """Main entry point of Buildnis.

    Parses commandline arguments and runs the program.
    """
    commandline_args, logger = setCmdLineArgsLogger()

    project_cfg_dir = commandline_args.conf_dir

    project_cfg_dir, config_dir_config = setUpConfDir(
        commandline_args, logger, project_cfg_dir
    )

    # Always create host config
    host_cfg, host_cfg_filename = setUpHostCfg(
        config_values.g_list_of_generated_files, logger, project_cfg_dir
    )

    (
        host_cfg_filename_exists,
        host_cfg_filename,
        build_tools_filename_exists,
        build_tools_filename,
        project_dep_filename_exists,
        project_dep_filename,
        project_config_filename_exists,
        project_config_filename,
    ) = setUpPaths(
        project_cfg_dir=project_cfg_dir,
        host_cfg_file=host_cfg_filename,
        list_of_generated_files=config_values.g_list_of_generated_files,
        host_cfg=host_cfg,
    )

    if not commandline_args.do_clean:
        host_cfg.writeJSON(json_path=host_cfg_filename)
        config_values.g_list_of_generated_files.append(host_cfg_filename)

        if not build_tools_filename_exists or commandline_args.do_configure == True:
            check_buildtools = check.Check(
                os_name=host_cfg.os, arch=host_cfg.cpu_arch
            )

            check_buildtools.writeJSON(json_path=build_tools_filename)
            if not build_tools_filename_exists:
                config_values.g_list_of_generated_files.append(build_tools_filename)

            logger.debug('Build tool config: """{cfg}"""'.format(cfg=check_buildtools))

        else:
            logger.warning(
                'JSON file "{path}" already exists, not checking for build tool configurations'.format(
                    path=build_tools_filename
                )
            )

        if project_config_filename_exists and commandline_args.do_configure == True:
            try:
                pathlib.Path(project_config_filename).unlink()
                project_config_filename_exists = False
            except Exception as excp:
                logger.error(
                    'error "{error}" deleting generated project config file to reconfigure project'.format(
                        error=excp
                    )
                )

        cfg = config.Config(
            project_config=commandline_args.project_config_file,
            json_path=project_config_filename,
        )

        cfg.project_dep_cfg = project_dependency.ProjectDependency(
            cfg.project_dependency_config, json_path=project_dep_filename
        )

        cfg.expandAllPlaceholders()

        if not project_dep_filename_exists or commandline_args.do_configure == True:
            cfg.checkDependencies(force_check=True)

        else:
            logger.warning(
                'JSON file "{path}" already exists, not checking project dependencies'.format(
                    path=project_dep_filename
                )
            )
            cfg.checkDependencies(force_check=False)

        cfg.project_dep_cfg.writeJSON()

        if not project_dep_filename_exists:
            config_values.g_list_of_generated_files.append(project_dep_filename)

        logger.debug('Project config: """{cfg}"""'.format(cfg=cfg))
        logger.debug(
            'Project dependency config: """{cfg}"""'.format(cfg=cfg.project_dep_cfg)
        )

        cfg.setBuildToolCfgPath(build_tools_filename)
        cfg.setHostConfigPath(host_cfg_filename)

        cfg.writeJSON()
        if not project_config_filename_exists:
            config_values.g_list_of_generated_files.append(project_config_filename)

        config_dir_config.writeJSON()

    else:
        logger.warning(
            'Not doing anything but deleting files, a "clean" argument ("--clean" or "--distclean") has been given!'
        )

    #! WARNING: no more logging after this function!
    # Logger is shut down
    doDistClean(
        commandline_args=commandline_args,
        logger=logger,
        list_of_generated_files=config_values.g_list_of_generated_files,
        list_of_generated_dirs=config_values.g_list_of_generated_dirs,
    )

    sys.exit(EXT_OK)


################################################################################
def setUpConfDir(commandline_args, logger, project_cfg_dir):
    working_dir = os.path.abspath(os.path.dirname(commandline_args.project_config_file))
    config_dir_filename = "/".join([working_dir, CFG_DIR_NAME])
    config_dir_filename = ".".join([config_dir_filename, "json"])
    config_dir_filename = os.path.abspath(config_dir_filename)
    config_dir_config = ConfigDirJson(
        file_name=config_dir_filename, working_dir=working_dir, cfg_path=project_cfg_dir
    )
    config_values.g_list_of_generated_files.append(config_dir_config.json_path)
    project_cfg_dir = config_dir_config.cfg_path
    if project_cfg_dir != working_dir:
        config_values.g_list_of_generated_dirs.append(project_cfg_dir)
    logger.info(
        'Setting project configuration directory to "{path}"'.format(
            path=project_cfg_dir
        )
    )
    return project_cfg_dir, config_dir_config


################################################################################
def setUpPaths(
    project_cfg_dir: FilePath,
    host_cfg_file: FilePath,
    list_of_generated_files: List[FilePath],
    host_cfg: Host,
) -> Tuple[bool, FilePath, bool, FilePath, bool, FilePath, bool, FilePath]:
    """Helper: set up all pathnames of JSON files.

    Args:
        project_cfg_dir (FilePath): The path to the directory the JSON files are generated in
        host_cfg (FilePath): The path to the generated host configuration JSON file
        list_of_generated_files (List[FilePath]): List of generated JSON files
        host_cfg (host_config.Host): host configuration object instance

    Returns:
        Tuple[bool, FilePath, bool, FilePath, bool, FilePath]: the paths to the JSON
            files and a bool that is `True` if the file already has been created.
    """
    host_cfg_filename_exists = False

    try:
        if checkIfIsFile(host_cfg_file) == True:
            list_of_generated_files.append(host_cfg_file)
            host_cfg_filename_exists = True
    except:
        pass

    build_tools_filename_exists = False

    build_tools_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    build_tools_filename = "_".join([build_tools_filename, BUILD_TOOL_CONFIG_NAME])
    build_tools_filename = ".".join([build_tools_filename, "json"])
    build_tools_filename = os.path.normpath(build_tools_filename)

    try:
        if checkIfIsFile(build_tools_filename) == True:
            list_of_generated_files.append(build_tools_filename)
            build_tools_filename_exists = True
    except:
        pass

    project_dep_filename_exists = False

    project_dep_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    project_dep_filename = "_".join([project_dep_filename, PROJECT_DEP_FILE_NAME])
    project_dep_filename = ".".join([project_dep_filename, "json"])
    project_dep_filename = os.path.normpath(project_dep_filename)

    try:
        if checkIfIsFile(project_dep_filename) == True:
            list_of_generated_files.append(project_dep_filename)
            project_dep_filename_exists = True
    except:
        pass

    project_config_filename_exists = False

    project_config_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    project_config_filename = "_".join([project_config_filename, PROJECT_FILE_NAME])
    project_config_filename = ".".join([project_config_filename, "json"])
    project_config_filename = os.path.normpath(project_config_filename)

    try:
        if checkIfIsFile(project_config_filename) == True:
            list_of_generated_files.append(project_config_filename)
            project_config_filename_exists = True
    except:
        pass

    return (
        host_cfg_filename_exists,
        host_cfg_file,
        build_tools_filename_exists,
        build_tools_filename,
        project_dep_filename_exists,
        project_dep_filename,
        project_config_filename_exists,
        project_config_filename,
    )


################################################################################
def doDistClean(
    commandline_args: object,
    logger: logging.Logger,
    list_of_generated_files: List[FilePath],
    list_of_generated_dirs: List[FilePath],
) -> None:
    """Helper: if argument `distclean` is set, delete all generated files.

    WARNING: Shuts down the logging mechanism, no more logging after this function!

    Args:
        commandline_args (object): Command line argument object instance
        logger (logging.Logger): The logger to use and stop
        list_of_generated_files (List[FilePath]): The list of files to delete
        list_of_generated_dirs (List[FilePath]): The list of directories to delete.
                            Attention: each directory must be empty!
    """
    if commandline_args.do_distclean == True:
        try:
            for file_path in list_of_generated_files:
                logger.warning(
                    'distclean: deleting file "{name}"'.format(name=file_path)
                )
                pathlib.Path(file_path).unlink(missing_ok=True)
            for dir_path in list_of_generated_dirs:
                logger.warning(
                    'distclean: deleting directory "{name}"'.format(name=dir_path)
                )
                pathlib.Path(dir_path).rmdir()
        except Exception as excp:
            logger.error(
                'error "{error}" trying to delete file "{name}"'.format(
                    error=excp, name=file_path
                )
            )

    logging.shutdown()

    try:
        if commandline_args.log_file != "" and commandline_args.log_file != None:
            print(
                'distclean: trying to delete logfile "{name}"'.format(
                    name=commandline_args.log_file
                )
            )
            pathlib.Path(commandline_args.log_file).unlink(missing_ok=True)
    except Exception as excp:
        print(
            'ERROR: distclean: error "{error}" trying to delete log file "{name}"'.format(
                error=excp, name=commandline_args.log_file
            ),
            file=sys.sys.stderr,
        )


################################################################################
def setUpHostCfg(
    list_of_generated_files: List[FilePath],
    logger: logging.Logger,
    project_cfg_dir: FilePath,
) -> Tuple[Host, FilePath]:
    """Helper: Sets up the host's configuration.

    Is always generated.

    Args:
        list_of_generated_files (List[FilePath]): The list of generated files to add to
        logger (logging.Logger): The logger to use
        project_cfg_dir (FilePath): Path to the project config JSON file

    Returns:
        Tuple[Host, FilePath]: the host configuration object instance and the host
                    configuration's filename as a tuple
    """
    host_cfg = Host()

    host_cfg_filename = "/".join([project_cfg_dir, host_cfg.host_name])
    host_cfg_filename = "_".join([host_cfg_filename, HOST_FILE_NAME])
    host_cfg_filename = ".".join([host_cfg_filename, "json"])
    host_cfg_filename = os.path.normpath(host_cfg_filename)

    logger.debug('Host config: """{cfg}"""'.format(cfg=host_cfg))

    return host_cfg, host_cfg_filename


################################################################################
def setCmdLineArgsLogger() -> Tuple[object, logging.Logger]:
    """Helper function: parses the command line, sets up the logger.

    Returns:
        Tuple[object, logging.Logger]: The commandline object instance and the
        logger instance to use
    """
    commandline_args = parseCommandLine()

    logger = getProgramLogger(commandline_args.log_level, commandline_args.log_file)

    pretty_args = pprint.pformat(commandline_args.__dict__, indent=4, sort_dicts=False)
    logger.debug('Commandline arguments: "{args}"'.format(args=pretty_args))

    logger.info(
        'Setting log level to "{lvl}"'.format(
            lvl=logging.getLevelName(commandline_args.log_level)
        )
    )

    logger.warning(
        'Using project config "{config}"'.format(
            config=commandline_args.project_config_file
        )
    )

    return commandline_args, logger


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    main()
