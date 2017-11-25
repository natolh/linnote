#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement assessments and related tools.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from operator import attrgetter
from pandas import read_excel
from linnote.student import Student


class Mark(object):
    """Student's mark to an assessment."""

    def __init__(self, student, assessment, score, scale=1, bonus=0):
        """Create a new mark."""
        super(Mark, self).__init__()
        self.student = student
        self.assessment = assessment
        self._raw = score / scale
        self._bonus = bonus / scale

    def __repr__(self):
        return '<Mark of {}: {}>'.format(self.student, self.value)

    @property
    def raw(self):
        return self._raw * self.assessment.coefficient

    @property
    def bonus(self):
        return self._bonus * self.assessment.coefficient

    @property
    def value(self):
        """The processed mark, including bonus points."""
        return (self._raw + self._bonus) * self.assessment.coefficient


class Assessment(object):
    """Evaluation of students knowledge."""

    def __init__(self, scale, coefficient, precision, src=None):
        """
        Initialize a new assessment.

        - scale:        Float. Actual scale in results file.
        - coefficient:  Float. Desired scale for output.
        - precision:    Integer. Number of decimals for outputing marks.
        - src:          Path-like object. Path pointing to the results file.

        Return: None.
        """
        super().__init__()
        self.scale = scale
        self.coefficient = coefficient
        self.precision = precision
        self.results = self.load_results(src) if src else list()

    @classmethod
    def create(cls, src):
        print(src.name)
        scale = float(input('Barème :'))
        coefficient = int(input('Coefficient :'))
        precision = int(input('Précision :'))
        return cls(scale=scale, coefficient=coefficient, precision=precision,
                   src=src)

    def __repr__(self):
        return '<Assessment>'

    def adjust_marks(self):
        maximum = max([mark._raw for mark in self.results])
        for mark in self.results:
            mark._bonus = (mark._raw / maximum) - mark._raw

    def load_results(self, file):
        results = read_excel(file, names=['anonymat', 'note'], usecols=1)
        results.dropna(how='all')

        stack = list()
        for result in results.to_dict('records'):
            student = Student(int(result['anonymat']))
            mark = Mark(student, self, float(result['note']), self.scale)
            stack.append(mark)

        return stack

    @staticmethod
    def aggregate_results(tests, test):
        by_student = attrgetter('student')

        results = [mark for test in tests for mark in test.results]
        results.sort(key=by_student)

        for student, marks in groupby(results, by_student):
            marks = list(marks)

            if len(marks) == len(tests):
                mark = Mark(student, test, sum([mark.value for mark in marks]),
                            test.coefficient)
                test.results.append(mark)
