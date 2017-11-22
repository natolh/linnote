#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement evaluation.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from time import sleep
from itertools import groupby
from time import strptime, strftime
from pandas import read_excel
from linnote.configuration import root
from linnote.result import Result
from linnote.student import Student, Group
from linnote.table import Table
from linnote.utils import make_stats


class Evaluation(object):

    def __init__(self):
        super(Evaluation, self).__init__()
        self.tables = list()

        # Create tables.
        for group_definition in Group.find():
            # Create group.
            students = Group.load(group_definition)
            name = group_definition.stem
            group = Group(students, name)

            # Create table.
            table = Table(self, group)
            self.tables.append(table)

    def adjust_marks(self):
        maximum = make_stats([result.raw_mark for result in self.results])[
            'maximum']
        for result in self.results:
            result.adjusted_mark = (
                result.raw_mark / maximum) * self.coefficient

        return self.results

    def grade(self):
        for table in self.tables:
            table.grade()

        return self.tables

    def results_to_table(self):
        for table in self.tables:
            table.results = list(
                filter(lambda r: r.student in table.group, self.results))

        return self.results


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
        results = sorted(
            [result for test in self.tests for result in test.results], key=lambda r: r.student)

        for student, results in groupby(results, key=lambda r: r.student):
            results = list(results)
            if len(results) == len(self.tests):
                result = Result(
                    student=student,
                    mark=sum([result.adjusted_mark for result in results])
                )
                self.results.append(result)
            else:
                pass

    def export_tables(self):
        for table in self.tables:
            table.export(
                template='assessment.html',
                precision=self.precision
            )

    def process(self):
        for test in Test.find():
            test = Test.create(assessment=self, src=test)
            self.tests.append(test)
            test.process()
            sleep(2)

        self.aggregate_results()
        self.results_to_table()
        self.grade()
        self.export_tables()


class Test(Evaluation):

    def __init__(self, assessment, label, date, scale, coefficient, precision, src):
        super(Test, self).__init__()
        self.assessment = assessment
        self.label = label
        self.date = date
        self.scale = scale
        self.coefficient = coefficient
        self.precision = precision
        self.results = self.load_results(src)

    @classmethod
    def create(cls, assessment, src):
        print(src.name)
        label = input('Référence : ')
        date = strptime(input('Date (DD/MM/YYYY) : '), '%d/%m/%Y')
        scale = float(input('Barème : '))
        coefficient = int(input('Coefficient : '))
        precision = int(input('Précision : '))
        return cls(assessment=assessment,
                   label=label, date=date,
                   scale=scale,
                   coefficient=coefficient,
                   precision=precision,
                   src=src)

    @classmethod
    def find(cls):
        return root.joinpath('results').glob('*.xlsx')

    @property
    def name(self):
        return 'Classement {0} du {1}'.format(self.label, strftime('%A %d %B %Y', self.date))

    def __repr__(self):
        return '<Test>'

    def export_tables(self):
        for table in self.tables:
            table.export(
                template='test.html',
                precision=self.precision
            )

    def load_results(self, src):
        document = read_excel(
            src,
            names=['anonymat', 'note'],
            usecols=1,
        ).dropna(how='all')
        return [Result(student=Student(identifier=int(result['anonymat'])), mark=(result['note'] / self.scale) * self.coefficient) for result in document.to_dict('records')]

    def process(self):
        self.adjust_marks()
        self.results_to_table()
        self.grade()
        self.export_tables()
