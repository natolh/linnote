#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Configuration.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from configparser import ConfigParser


def load(config_path):
    """
    Load configuration from INI file.

    - configfile:   A pathlike object. Path to the configuration file default to
                    the file named 'configuration.ini' in the app directory.

    Return: A config object.
    """
    configuration = ConfigParser()
    configuration.read(config_path)
    return configuration
