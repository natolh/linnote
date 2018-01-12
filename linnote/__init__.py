#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Ranking tool for mock assessment of French first year health students.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

import matplotlib
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
matplotlib.use('Agg')
