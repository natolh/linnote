#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement evaluation.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from operator import attrgetter
from time import strptime, strftime
from pandas import read_excel
from linnote.result import Mark
from linnote.student import Student, Group
from linnote.ranking import Ranking, Rank


class Evaluation(object):

    def __init__(self):
        super(Evaluation, self).__init__()
        self.rankings = list()

        # Create rankings.
        for group_definition in Group.find():
            # Create group.
            students = Group.load(group_definition)
            name = group_definition.stem
            group = Group(students, name)

            # Create a ranking.
            ranking = Ranking(self, group)
            self.rankings.append(ranking)

    def adjust_marks(self):
        maximum = max([mark.raw for mark in self.results])
        for mark in self.results:
            mark.bonus = (mark.raw / maximum) - mark.raw

    def grade(self):
        for ranking in self.rankings:
            ranking.rank()

    def results_to_ranking(self):
        for ranking in self.rankings:
            marks = filter(lambda m: m.student in ranking.group, self.results)
            for mark in marks:
                rank = Rank(mark.student.identifier, mark.raw * self.coefficient, adj=mark.value * self.coefficient)
                ranking.ranks.append(rank)


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
    def name(self):
        return 'Session N°{}'.format(self.identifier)

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
                mark = Mark(student, sum([mark.value for mark in marks]), len(marks))
                self.results.append(mark)

    def export_rankings(self):
        for ranking in self.rankings:
            ranking.export(
                template='assessment.html',
                precision=self.precision
            )


class Test(Evaluation):

    def __init__(self, label, date, scale, coefficient, precision, src):
        super(Test, self).__init__()
        self.label = label
        self.date = date
        self.scale = scale
        self.coefficient = coefficient
        self.precision = precision
        self.results = self.load_results(src)

    @classmethod
    def create(cls, src):
        print(src.name)
        label = input('Référence : ')
        date = strptime(input('Date (DD/MM/YYYY) : '), '%d/%m/%Y')
        scale = float(input('Barème : '))
        coefficient = int(input('Coefficient : '))
        precision = int(input('Précision : '))
        return cls(label=label, date=date, scale=scale,
                   coefficient=coefficient, precision=precision, src=src)

    @property
    def name(self):
        return 'Classement {0} du {1}'.format(self.label, strftime('%A %d %B %Y', self.date))

    def __repr__(self):
        return '<Test>'

    def export_rankings(self):
        for ranking in self.rankings:
            ranking.export(
                template='test.html',
                precision=self.precision
            )

    def load_results(self, file):
        results = read_excel(file, names=['anonymat', 'note'], usecols=1)
        results.dropna(how='all')

        stack = list()
        for result in results.to_dict('records'):
            student = Student(int(result['anonymat']))
            mark = Mark(student, float(result['note']), self.scale)
            stack.append(mark)

        return stack
