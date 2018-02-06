#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Ranking tool for mock assessment of French first year health students.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pathlib import Path
import matplotlib


APP_DIR = Path(__file__).resolve().parent
matplotlib.use('Agg')
