#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Ranking tools for mock assessment of French first year health students. 

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from locale import setlocale, LC_ALL
from pathlib import Path
from linnote.configuration import LOCALE


setlocale(LC_ALL, LOCALE)
APP_DIR = Path(__file__).resolve().parents[1]
