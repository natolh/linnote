#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement table.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from pandas import read_excel
from linnote.configuration import root
from linnote.student import Student
from linnote.utils import make_stats, render_template, make_histogram


class Table(object):
    """A group of student and their results to a test or an assessment."""

    def __init__(self, evaluation, group_name, src=None):
        super(Table, self).__init__()
        self.evaluation = evaluation
        self.group_name = group_name
        self.students = self.assign(src) if src else None
        self.results = list()

    @classmethod
    def find(cls):
        """
        Find files describing student's groups.

        Each group of student will generate a standalone table so that students
        of different groups will be grade in different tables.
        """
        # Return an iterable containing all group description files path
        # objects.
        return root.joinpath("groups").glob("*.xlsx")

    @property
    def name(self):
        return "{0} - {1}".format(self.evaluation.name, self.group_name)

    def __repr__(self):
        return "<Table {0} | {1} students>".format(self.name, len(self.students))

    def assign(self, src):
        """
        Assign students to a table instance.

        Students list is loaded from a file.
        """
        # Open the group description files and parse it.
        document = read_excel(src, names=["anonymat"])

        # For each student list in the group description file create a student
        # object and append it to the students list of the table. Then return
        # students.
        return [Student(identifier=student["anonymat"]) for student in document.to_dict("records")]

    def export(self, template, **kwargs):
        """Export table to an HTML document."""
        output = render_template(
            template=template,
            table=self,
            evaluation=self.evaluation,
            statistics=make_stats([result.raw_mark for result in self.results]),
            histogram=make_histogram([result.raw_mark for result in self.results], self.evaluation.coefficient),
            **kwargs)

        document = root.joinpath("tables", self.name).with_suffix(".html")
        document.write_bytes(output)

    def grade(self):
        """Grade student's results for students of the group."""
        # Sorting in place student's results (by marks here) because the
        # groupby method need the iterable to be sort on the key you want to
        # group (by marks here).
        self.results.sort(key=lambda r: r.raw_mark, reverse=True)

        # Enumerate student's results by group of equal marks, so that results
        # with equal marks will be grade with equal ranks
        offset = 0

        for rank, (_, group) in enumerate(groupby(self.results, lambda x: x.raw_mark), start=1):

            for _, result in enumerate(group):

                if _ > 0:
                    offset += 1
                result.rank = sum([rank, offset]) if _ < 1 else sum(
                    [rank, offset - _])

        # Return sorted and graded student's results.
        return self.results
