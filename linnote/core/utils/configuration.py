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


def locate(configuration_path: Union[str, Path]) -> Path:
    """
    Locate a configuration file and return it in the form of a Path object.

    If the path provided is not absolute, the path is assumed to be relative
    to the current working directory.
    """
    root = Path.cwd()
    configuration_path = Path(configuration_path)
    if not configuration_path.is_absolute():
        configuration_path = root.joinpath(configuration_path)
    return configuration_path

def load(configuration_path: Union[str, Path]) -> ConfigParser:
    """
    Load a configuration file.

    If the path provided is not absolute, the path is assumed to be relative
    to the current working directory. See 'locate' function for further
    details.
    """
    configuration_file = locate(configuration_path)
    configuration = ConfigParser()
    configuration.read(configuration_file)
    return configuration

def save(configuration_path: Union[str, Path], configuration: ConfigParser):
    """
    Save the configuration.
    """
    configuration_file = locate(configuration_path)
    configuration.write(configuration_file.open('w'))
