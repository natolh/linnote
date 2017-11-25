#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement composers for creating reports.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


from opertator import attrgetter
from statistics import mean, median

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
