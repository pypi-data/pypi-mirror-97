# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     host.py
# Date:     15.Feb.2021
###############################################################################

from __future__ import annotations


import platform

from buildnis.modules.config.json_base_class import JSONBaseClass
from buildnis.modules.helpers.files import checkIfExists
from buildnis.modules.helpers.execute import runCommand
from buildnis.modules.config import (
    AMD64_ARCH_STRING,
    CFG_VERSION,
    HOST_FILE_NAME,
    LINUX_OS_STRING,
    OSX_NAME_DICT,
    OSX_OS_STRING,
    WINDOWS_OS_STRING,
    config_values,
)


class Host(JSONBaseClass):
    """Holds all information about the host this is running on.

    Stores hostname, OS, OS version, CPU architecture, RAM, CPU name, ...

    Attributes:
        host_name (str):      This host's name
        os (str):             The OS this is running on (like "Windows", "Linux")
        os_vers_major (str):  Major version of the OS (like "10" for Windows 10)
        os_vers (str):        Excact version string
        cpu_arch (str):       CPU architecture, like "x64" or "x86"
        cpu (str):            The detailed name of the CPU
        file_name (str):      The JSON identifier of the host config file, part
                              of the file name
        level2_cache (int):   Size of the CPU's level 2 cache, in bytes
        level3_cache (int):   Size of the CPU's level 3 cache, in bytes
        num_cores (int):      The number of physical cores
        num_logical_cores (int): The number of logical, 'virtual' cores
        ram_total (int):      Amount of physical RAM in bytes
        gpu List[str]:        The list of names of all GPUs
        python_version (str): The version of this host's Python interpreter
        json_path(str):       The path to the written JSON host config file

    Methods:
        collectWindowsConfig: adds information, that has to be collected in a
                            Windows specific way
        collectLinuxConfig: adds information, that has to be collected in a
                            Linux specific way
        collectOSXConfig:   adds information, that has to be collected in a
                            Mac OS X specific way
    """

    ###########################################################################
    def __init__(self) -> None:
        """Constructor of class Host, gathers and sets the host's environment.

        Like OS, hostname, OS version, CPU architecture, ...
        """
        super().__init__(config_file_name=HOST_FILE_NAME, config_name="host")

        self._logger.info("Gathering information about this host ...")

        self.file_name = HOST_FILE_NAME
        self.file_version = ".".join(CFG_VERSION)

        (
            self.os,
            self.host_name,
            self.os_vers_major,
            self.os_vers,
            self.cpu_arch,
            self.cpu,
        ) = platform.uname()
        if self.os == "Darwin":
            self.os = OSX_OS_STRING
        if self.cpu_arch == "AMD64" or self.cpu_arch == "x86_64":
            self.cpu_arch = AMD64_ARCH_STRING

        self.python_version = platform.python_version()

        if self.os == WINDOWS_OS_STRING:
            self.collectWindowsConfig()

        elif self.os == LINUX_OS_STRING:
            self.collectLinuxConfig()

        elif self.os == OSX_OS_STRING:
            self.collectOSXConfig()

        else:
            self._logger.error(
                'error, "{os_name}" is a unknown OS!'.format(os_name=self.os)
            )
            self._logger.error(
                'You can add support of this OS to the file "modules\config\host.py"'
            )
            self._logger.error("")

        # set global constants
        config_values.HOST_OS = self.os
        config_values.HOST_CPU_ARCH = self.cpu_arch
        config_values.HOST_NAME = self.host_name
        config_values.HOST_NUM_CORES = self.num_cores
        config_values.HOST_NUM_LOG_CORES = self.num_logical_cores

    #############################################################################
    def collectWindowsConfig(self) -> None:
        """Collect information about the hardware we're running on on Windows.

        Calls these commands and parses their outputs:

        wmic cpu get L2CacheSize,L3CacheSize,NumberOfLogicalProcessors,NumberOfCores,Name
        wmic memorychip get capacity
        wmic path win32_VideoController get name
        """
        try:
            cpu_info_cmd = runCommand(
                exe="wmic",
                args=[
                    "cpu",
                    "get",
                    "L2CacheSize,L3CacheSize,NumberOfLogicalProcessors,NumberOfCores",
                ],
            )
            for line in cpu_info_cmd.std_out.strip().split("\n"):
                if "L2CacheSize" in line:
                    continue
                if line != "":
                    (
                        level2_cache,
                        level3_cache,
                        num_cores,
                        num_logical_cores,
                    ) = line.split()
                    try:
                        self.level2_cache = int(level2_cache)
                        self.level3_cache = int(level3_cache)
                        self.num_cores = int(num_cores)
                        self.num_logical_cores = int(num_logical_cores)
                    except:
                        pass

            cpu_name_cmd = runCommand(exe="wmic", args=["cpu", "get", "Name"])
            for line in cpu_name_cmd.std_out.strip().split("\n"):
                if "Name" in line:
                    continue
                if line != "":
                    self.cpu = line

            gpu_info_cmd = runCommand(
                exe="wmic", args=["path", "win32_VideoController", "get", "name"]
            )
            self.gpu = []
            for line in gpu_info_cmd.std_out.strip().split("\n"):
                if "Name" in line:
                    continue
                if line != "":
                    self.gpu.append(line.strip())

            mem_info_cmd = runCommand(
                exe="wmic", args=["memorychip", "get", "capacity"]
            )
            self.ram_total = 0
            for line in mem_info_cmd.std_out.strip().split("\n"):
                if "Capacity" in line:
                    continue
                if line != "":
                    try:
                        self.ram_total += int(line)
                    except:
                        pass

        except Exception as excp:
            self._logger.error('error "{error}" calling wmic'.format(error=excp))

    #############################################################################
    def collectLinuxConfig(self) -> None:
        """Collect information about the hardware we're running on on Linux.

        Calls the following commands:

        cat /etc/os-release
        NAME="Red Hat Enterprise Linux"
        VERSION="8.3 (Ootpa)"

        grep "model name" /proc/cpuinfo |uniq|cut -d':' -f2
        getconf -a|grep LEVEL2_CACHE_SIZE|awk '{print $2}'
        getconf -a|grep LEVEL3_CACHE_SIZE|awk '{print $2}'
        grep "cpu cores" /proc/cpuinfo |uniq|cut -d':' -f2
        grep "siblings" /proc/cpuinfo |uniq |cut -d':' -f2
        free -b|grep "Mem:"|awk '{print $2}'
        grep "DISTRIB_DESCRIPTION" /etc/lsb-release
        lspci|grep VGA|cut -f3 -d':'
        """
        try:
            try:
                if checkIfExists("/etc/os-release") == True:
                    os_vers_maj = runCommand(
                        exe="bash",
                        args=[
                            "-c",
                            "grep NAME /etc/os-release |head -1|cut -d'=' -f2|tr -d '\"'",
                        ],
                    )
                    self.os_vers_major = os_vers_maj.std_out.strip()

                    os_vers = runCommand(
                        exe="bash",
                        args=[
                            "-c",
                            "grep VERSION /etc/os-release |head -1|cut -d'=' -f2|tr -d '\"'",
                        ],
                    )
                    self.os_vers = os_vers.std_out.strip()
            except:
                pass

            cpu_name_cmd = runCommand(
                exe="bash",
                args=["-c", "grep 'model name' /proc/cpuinfo |head -1|cut -d':' -f2-"],
            )
            self.cpu = cpu_name_cmd.std_out.strip()

            cpu_num_cores = runCommand(
                exe="bash",
                args=["-c", "grep 'cpu cores' /proc/cpuinfo |uniq|cut -d':' -f2"],
            )
            self.num_cores = int(cpu_num_cores.std_out.strip())

            cpu_num_log_cpus = runCommand(
                exe="bash",
                args=["-c", "grep siblings /proc/cpuinfo |uniq |cut -d':' -f2"],
            )
            self.num_logical_cores = int(cpu_num_log_cpus.std_out.strip())

            cpu_l2_cache = runCommand(
                exe="bash",
                args=["-c", "getconf -a|grep LEVEL2_CACHE_SIZE|awk '{print $2}'"],
            )
            self.level2_cache = int(cpu_l2_cache.std_out.strip())

            cpu_l3_cache = runCommand(
                exe="bash",
                args=["-c", "getconf -a|grep LEVEL3_CACHE_SIZE|awk '{print $2}'"],
            )
            self.level3_cache = int(cpu_l3_cache.std_out.strip())

            ram_size = runCommand(
                exe="bash", args=["-c", "free -b|grep 'Mem:'|awk '{print $2}'"]
            )
            self.ram_total = int(ram_size.std_out.strip())

            self.gpu = []
            gpu_info_cmd = runCommand(
                exe="bash", args=["-c", "lspci|grep VGA|cut -f3 -d':'"]
            )
            for line in gpu_info_cmd.std_out.strip().split("\n"):
                if line != "":
                    self.gpu.append(line.strip())

            if self.gpu == []:
                gpu_info_cmd = runCommand(
                    exe="bash", args=["-c", "/sbin/lspci|grep VGA|cut -f3 -d':'"]
                )
                for line in gpu_info_cmd.std_out.strip().split("\n"):
                    if line != "":
                        self.gpu.append(line.strip())

        except Exception as excp:
            self._logger.error(
                'error "{error}" getting Linux host information'.format(error=excp)
            )

    #############################################################################
    def collectOSXConfig(self) -> None:
        """Collect information about the hardware we're running on on MacOS X.

        Using this commands:
        sysctl -n hw.memsize
        sysctl -n hw.physicalcpu
        sysctl -n hw.logicalcpu
        sysctl -n hw.l2cachesize
        sysctl -n hw.l3cachesize
        sysctl -n machdep.cpu.brand_string
        sw_vers -productVersion

        TODO get GPU info: system_profiler SPDisplaysDataType
        """
        try:
            os_name = runCommand(exe="sw_vers", args=["-productVersion"])
            self.os_vers = os_name.std_out.strip()

            os_vers_2_digits_list = self.os_vers.rsplit(".")
            self.os_vers_major = OSX_NAME_DICT[".".join(os_vers_2_digits_list[:-1])]

            cpu_name_cmd = runCommand(
                exe="sysctl", args=["-n", "machdep.cpu.brand_string"]
            )
            self.cpu = cpu_name_cmd.std_out.strip()

            cpu_num_cores = runCommand(exe="sysctl", args=["-n", "hw.physicalcpu"])
            self.num_cores = int(cpu_num_cores.std_out)

            cpu_num_log_cpus = runCommand(exe="sysctl", args=["-n", "hw.logicalcpu"])
            self.num_logical_cores = int(cpu_num_log_cpus.std_out)

            cpu_l2_cache = runCommand(exe="sysctl", args=["-n", "hw.l2cachesize"])
            self.level2_cache = int(cpu_l2_cache.std_out)

            cpu_l3_cache = runCommand(exe="sysctl", args=["-n", "hw.l3cachesize"])
            self.level3_cache = int(cpu_l3_cache.std_out)

            ram_size = runCommand(exe="sysctl", args=["-n", "hw.memsize"])
            self.ram_total = int(ram_size.std_out)

            self.gpu = []

        except Exception as excp:
            self._logger.error(
                'error "{error}" gathering information on OS X'.format(error=excp)
            )


################################################################################
def printHostInfo() -> None:
    """To test the collection of the host's information, print all to stdout."""
    print(Host())


################################################################################
if __name__ == "__main__":
    printHostInfo()
