"""
webspinner
----------
Python utilities for working with various dsgrid data sources

:copyright: (c) 2021, Alliance for Sustainable Energy, LLC
:license: BSD-3
"""

import configparser

from .__version__ import __version__

class WebspinnerRuntimeError(RuntimeError): pass

WEBSPINNER_CONFIGURATION = None

def configure(config_filename):
    """
    Configure webspinner by loading a config file with optional sections '[AWS]'
    and/or '[PGRES]'

    Parameters
    ----------
    config_filename : pathlib.Path or str
    """
    global WEBSPINNER_CONFIGURATION
    config = configparser.ConfigParser()
    config.read(config_filename)
    WEBSPINNER_CONFIGURATION = config
