#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ranking tools.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from itertools import groupby
from operator import attrgetter
from linnote.configuration import root
from linnote.utils import make_stats, render_template, make_histogram


class Ranking(object):
    """A ranked list of students results to an assessment."""

    def __init__(self, evaluation, group):
        """
        Create a new ranking.

        - evaluation:   An 'evaluation.Evaluation' object. The results to rank.
        - group:        A 'student.Group' object. The list of students to rank.

        Return: None.
        """
        super(Ranking, self).__init__()
        self.evaluation = evaluation
        self.group = group
        self.ranks = list()

    @property
    def name(self):
        return '{} - {}'.format(self.evaluation.name, self.group.name)

    def __repr__(self):
        return '<Ranking {}>'.format(self.name)

    def export(self, template, **kwargs):
        """Export ranking to an HTML document."""
        output = render_template(
            template=template,
            ranking=self,
            evaluation=self.evaluation,
            statistics=make_stats([rank.score for rank in self.ranks]),
            histogram=make_histogram([rank.score for rank in self.ranks], self.evaluation.coefficient),
            **kwargs)

        document = root.joinpath("rankings", self.name).with_suffix(".html")
        document.write_bytes(output)

    def rank(self):
        """Compute ranks."""
        # Sorting in place student's results (by marks here) because the
        # groupby method need the iterable to be sort on the key you want to
        # group (by marks here).
        score = attrgetter('score')
        self.ranks.sort(key=score, reverse=True)

        # Enumerate student's results by group of equal marks, so that results
        # with equal marks will be grade with equal ranks
        offset = 0

        for pos, (_, group) in enumerate(groupby(self.ranks, score), start=1):

            for _, rank in enumerate(group):

                if _ > 0:
                    offset += 1

                rank.position = sum([pos, offset]) if _ < 1 else sum(
                    [pos, offset - _])


class Rank(object):
    """Student's rank to an evaluation."""

    def __init__(self, identifier, score, position=None, **kwargs):
        super(Rank, self).__init__()
        self.identifier = identifier
        self.score = score
        self.position = position
        self.kwargs = kwargs

    def __repr__(self):
        return '<Rank of {}: {}>'.format(self.identifier, self.position)
