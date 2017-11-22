#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement marks.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


class Mark(object):
    """Student's mark to an evaluation."""

    def __init__(self, student, score, scale=1, bonus=0):
        """Create a new mark."""
        super(Mark, self).__init__()
        self.student = student
        self.raw = score / scale
        self.bonus = bonus / scale

    def __repr__(self):
        return '<Mark of {}: {}>'.format(self.student, self.value)

    @property
    def value(self):
        """The processed mark, including bonus points."""
        return self.raw + self.bonus
