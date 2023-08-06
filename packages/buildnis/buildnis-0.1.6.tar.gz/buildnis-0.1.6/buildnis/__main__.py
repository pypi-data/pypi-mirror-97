#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     buildnis.py
# Date:     13.Feb.2021
###############################################################################

# This is just a wrapper to catch when running using python 2. The real `main`
# is in `modules/main.py`.

from __future__ import print_function

import sys
import platform

if sys.version_info.major < 3 or sys.version_info.minor < 8:
    print(
        "ERROR: Python version is too old, I need at least Python 3.8, this has a version of {version}".format(
            version=platform.python_version()
        ),
        file=sys.stderr,
    )
    sys.exit(1)

################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    from buildnis.modules import main
    
    main.main()
    
