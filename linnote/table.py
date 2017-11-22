#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement table.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from linnote.configuration import root
from linnote.utils import make_stats, render_template, make_histogram


class Table(object):
    """A group of student and their results to a test or an assessment."""

    def __init__(self, evaluation, group):
        super(Table, self).__init__()
        self.evaluation = evaluation
        self.group = group
        self.results = list()

    @property
    def name(self):
        return "{0} - {1}".format(self.evaluation.name, self.group.name)

    def __repr__(self):
        return "<Table {0} | {1} students>".format(self.name, len(self.group))

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
