#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement marks.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


class Mark(object):
    """Student's mark to an evaluation."""

    def __init__(self, student, evaluation, score, scale=1, bonus=0):
        """Create a new mark."""
        super(Mark, self).__init__()
        self.student = student
        self.evaluation = evaluation
        self._raw = score / scale
        self._bonus = bonus / scale

    def __repr__(self):
        return '<Mark of {}: {}>'.format(self.student, self.value)

    @property
    def raw(self):
        return self._raw * self.evaluation.coefficient

    @property
    def bonus(self):
        return self._bonus * self.evaluation.coefficient

    @property
    def value(self):
        """The processed mark, including bonus points."""
        return (self._raw + self._bonus) * self.evaluation.coefficient
