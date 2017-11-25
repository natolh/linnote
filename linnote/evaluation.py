#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement evaluation.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from operator import attrgetter
from pandas import read_excel
from linnote.result import Mark
from linnote.student import Student


class Evaluation(object):

    def adjust_marks(self):
        maximum = max([mark._raw for mark in self.results])
        for mark in self.results:
            mark._bonus = (mark._raw / maximum) - mark._raw


class Assessment(Evaluation):

    def __init__(self, identifier):
        super(Assessment, self).__init__()
        self.identifier = identifier
        self.tests = list()
        self.results = list()

    @classmethod
    def create(cls):
        identifier = input('Session N° : ')
        return cls(identifier=identifier)

    @property
    def coefficient(self):
        return sum([test.coefficient for test in self.tests])

    @property
    def precision(self):
        return min([test.precision for test in self.tests])

    def __repr__(self):
        return '<Assessment #{}>'.format(self.identifier)

    def aggregate_results(self):
        by_student = attrgetter('student')

        results = [mark for test in self.tests for mark in test.results]
        results.sort(key=by_student)

        for student, marks in groupby(results, by_student):
            marks = list(marks)

            if len(marks) == len(self.tests):
                mark = Mark(student, self, sum([mark.value for mark in marks]), self.coefficient)
                self.results.append(mark)


class Test(Evaluation):

    def __init__(self, scale, coefficient, precision, src):
        super(Test, self).__init__()
        self.scale = scale
        self.coefficient = coefficient
        self.precision = precision
        self.results = self.load_results(src)

    @classmethod
    def create(cls, src):
        print(src.name)
        scale = float(input('Barème :'))
        coefficient = int(input('Coefficient :'))
        precision = int(input('Précision :'))
        return cls(scale=scale, coefficient=coefficient, precision=precision,
                   src=src)

    def __repr__(self):
        return '<Test>'

    def load_results(self, file):
        results = read_excel(file, names=['anonymat', 'note'], usecols=1)
        results.dropna(how='all')

        stack = list()
        for result in results.to_dict('records'):
            student = Student(int(result['anonymat']))
            mark = Mark(student, self, float(result['note']), self.scale)
            stack.append(mark)

        return stack
