#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Configuration.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from platform import system as plateform


LANGUAGE = 'fr_FR'
CHARSET = 'UTF-8'
LOCALE = 'French_France.1252' if plateform() == 'Windows' else 'fr_FR.UTF-8'
