#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tools to read INI configuration files.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from configparser import ConfigParser
from pathlib import Path
from typing import Union


def load(configuration_path: Union[str, Path]) -> ConfigParser:
    """
    Load a configuration file.

    If the path provided is not absolute, the path is assumed to be relative
    to the current working directory. If the path point to a directory or a
    non existent file a FileNotFoundError is raised by Path.open().
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
