#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement composers for creating reports.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from io import StringIO
from operator import attrgetter
from statistics import mean, median
from matplotlib import pyplot
from linnote.ranking import Ranking

value = attrgetter('value')


def statistics(assessment, group):
    marks = [value(m) for m in assessment.results if m.student in group]
    return {
        "size": len(marks),
        "maximum": max(marks, default=0),
        "minimum": min(marks, default=0),
        "mean": mean(marks) if marks else 0,
        "median": median(marks) if marks else 0
    }


def histogram(assessment, group):
    document = StringIO()
    coefficient = assessment.coefficient
    marks = [value(m) for m in assessment.results if m.student in group]

    pyplot.figure(figsize=(6, 4))
    pyplot.hist(marks, bins=coefficient, range=(0, coefficient),
                color=(0.80, 0.80, 0.80), histtype="stepfilled")
    pyplot.title("Répartition des notes")
    pyplot.savefig(document, format="svg")
    document.seek(0)
    return "\n".join(document.readlines()[5:-1])


def ranking(assessment, group):
    marks = [mark for mark in assessment.results if mark.student in group]
    return Ranking(marks, key=value)
