#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement ranking tools.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from functools import wraps
from itertools import groupby, repeat
from operator import attrgetter
from linnote.configuration import ROOT
from linnote.utils import make_stats, render_template, make_histogram


def ranker(f):
    @wraps(f)
    def wrapper(position, group):
        size = sum((1 for _ in group))
        rank, offset = f(position, size)
        return repeat(rank, size), offset
    return wrapper


@ranker
def HIGH(position, size):
    return position, size


@ranker
def LOW(position, size):
    return position + size - 1, size


@ranker
def AVERAGE(position, size):
    return position * (1 + size) / 2, size


@ranker
def SEQUENTIAL(position, size):
    return position, 1


def rank(items, key=None, reverse=True, start=1, handle=HIGH):
    """
    Generate ranks on the fly.

    - items:    Iterable. Collection of homogenous items to rank.
    - key:      Callable. Retrieve the key for ranking items.
    - reverse:  Boolean. If set to True, items are ranked by decreasing order ;
                if set to False items are ranked by increasing order.
    - start:    Integer. Starting rank.
    - handle:   Callable. A callable to determine rank for tied values and the
                next rank.

    Return: A list of Rank objects.
    """
    index = start
    items = sorted(items, key=key, reverse=reverse)

    for score, group in groupby(items):
        group = list(group)
        ranks, offset = handle(index, group)
        index += offset
        yield from zip(ranks, group)


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

    def __repr__(self):
        return '<Ranking: {}>'.format(self.name)

    @property
    def name(self):
        return '{} - {}'.format(self.evaluation.name, self.group.name)

    def export(self, template, **kwargs):
        """Export ranking to an HTML document."""
        output = render_template(
            template=template,
            ranking=self,
            evaluation=self.evaluation,
            statistics=make_stats([rank.score for rank in self.ranks]),
            histogram=make_histogram([rank.score for rank in self.ranks], self.evaluation.coefficient),
            **kwargs)

        document = ROOT.joinpath("rankings", self.name).with_suffix(".html")
        document.write_bytes(output)

    def make(self):
        """Build the ranking."""
        score = attrgetter('score')
        for r, item in rank(self.ranks, score):
            item.position = r


class Rank(object):
    """Student's rank to an evaluation."""

    def __init__(self, identifier, score, position=None, **kwargs):
        """
        Create a new rank.

        - identifier:   A string or an integer. Something to identify the
                        student.
        - score:        A sortable value. The score of the student to the
                        assessment. Used to establish the ranking.
        - position:     Integer. The student's position in the ranking.
        - kwargs:       Dictionnary. Extra informations.

        Return: None.
        """
        super(Rank, self).__init__()
        self.identifier = identifier
        self.score = score
        self.position = position
        self.kwargs = kwargs

    def __repr__(self):
        return '<Rank #{}: {}>'.format(self.position, self.score)
