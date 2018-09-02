#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Handle configuration file (INI-style).

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from configparser import ConfigParser
from pathlib import Path
from typing import Union


def load(configuration_path: Union[str, Path]) -> ConfigParser:
    """
    Load a configuration file.

    The path provided in 'configuration_path' should exist, point to a file
    and the file should be a valid configuration file (INI-style) to be parsed
    by ConfigParser. If the path is not absolute, the path is assumed to be
    relative to the current working directory.
    """
    configuration = ConfigParser()
    configuration_file = Path(configuration_path).open()
    configuration.read_file(configuration_file)
    return configuration

def save(configuration_path: Union[str, Path], configuration: ConfigParser):
    """
    Save the configuration.
    """
    configuration_file = Path(configuration_path).open('w')
    configuration.write(configuration_file)
