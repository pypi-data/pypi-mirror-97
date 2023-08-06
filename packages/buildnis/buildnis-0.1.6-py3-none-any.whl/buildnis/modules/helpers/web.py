# SPDX-License-Identifier: MIT
# Copyright (C) 2021 Roland Csaszar
#
# Project:  Buildnis
# File:     web.py
# Date:     21.Feb.2021
###############################################################################

from __future__ import annotations
import logging
import pathlib
import shutil
import urllib.request
from buildnis.modules.helpers import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


class WebException(Exception):
    """Exception that is raised from functions in this module."""

    pass


# TODO: make better
###############################################################################
def doDownload(url: str, to: str = "", use_proxy: bool = False) -> None:
    """Download data from the given URL to the given path.

    Args:
        url (str): The URL to download from
        to (str, optional): The path to save the download to. Defaults to "".
        use_proxy (bool, optional): Should a proxy be used. Defaults to False.
    """
    try:
        _logger.info(
            'Downloading data from "{url}" to "{path}" (using proxy: {proxy})'.format(
                url=url, path=to, proxy=use_proxy
            )
        )

        with urllib.request.urlopen(url) as url_response:
            for item in url_response.getheaders():
                print(item)
            with pathlib.Path(to).open(mode="bw") as dest:
                shutil.copyfileobj(url_response, dest)

    except Exception as excp:
        raise WebException(excp)
