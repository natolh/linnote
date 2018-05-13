#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from configparser import ConfigParser
from pathlib import Path
from linnote import APP_DIR


def load(config_path):
    """
    Load configuration from INI file.

    - configfile:   A pathlike object. Path to the configuration file default
                    to the file named 'configuration.ini' in the app directory.

    Return: A config object.
    """
    # Locate configuration file.
    config_path = Path(config_path)
    if not config_path.is_absolute():
        config_path = APP_DIR.parent.joinpath(config_path)

    configuration = ConfigParser()
    configuration.read(config_path)
    return configuration
