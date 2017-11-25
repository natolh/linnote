#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Miscellaneous tools for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from io import StringIO
from matplotlib import pyplot as plot


def histogram(assessment, group):
    """Distribution of marks to an assessment."""
    sample = [mark for mark in assessment.results if mark.student in group]
    coefficient = assessment.coefficient
    document = StringIO()
    plot.figure(figsize=(6, 4))
    plot.hist(x=sample, bins=coefficient, range=(0, coefficient),
              color=(0.80, 0.80, 0.80), histtype="stepfilled")
    plot.title("Répartition des notes")
    plot.savefig(document, format="svg")
    document.seek(0)
    return "\n".join(document.readlines()[5:-1])
