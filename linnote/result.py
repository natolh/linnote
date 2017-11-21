#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement results.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


class Result(object):
    """Represent a result."""

    def __init__(self, student, mark):
        super(Result, self).__init__()
        self.student = student
        self.raw_mark = mark
        self.adjusted_mark = float()
        self.rank = int()

    def __repr__(self):
        return '<Result of student #{}>'.format(self.student.identifier)
