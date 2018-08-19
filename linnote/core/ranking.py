#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ranking tools.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from functools import wraps
from itertools import groupby, repeat
from operator import attrgetter
from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
from .utils import BASE


def ranker(function):
    """Decorator for tie handling methods."""
    @wraps(function)
    def wrapper(position, group):
        """Wrapping function."""
        size = sum(1 for _ in group)
        rank, offset = function(position, size)
        return repeat(rank, size), offset
    return wrapper


@ranker
def high(position, size):
    """
    Tie handling function.

    Handle tie ranking using the 'Standard Competition' strategy defined here:
    https://en.wikipedia.org/wiki/Ranking. Tied values are assigned the current
    rank, the next available ranks is equal to the sum of the actual rank plus
    the number of tied values.

    Return: A tuple. First item is the rank for tied values ; second item is
            the offset to the next rank.
    """
    return position, size


@ranker
def low(position, size):
    """
    Tie handling function.

    Handle tie ranking using the 'Standard Competition' strategy defined here:
    https://en.wikipedia.org/wiki/Ranking. The next available ranks is equal to
    the sum of the actual rank plus the number of tied values, tied values are
    assigned this next rank minus one.

    Return: A tuple. First item is the rank for tied values ; second item is
            the offset to the next rank.
    """
    return position + size - 1, size


# Consider using decimal instead.
@ranker
def average(position, size):
    """
    Tie handling function.

    Handle tie ranking using the 'Standard Competition' strategy defined here:
    https://en.wikipedia.org/wiki/Ranking. The next available ranks is equal to
    the sum of the actual rank plus the number of tied values, tied values are
    assigned the arithmetic mean of the curent rank and the next rank.

    Return: A tuple. First item is the rank for tied values ; second item is
            the offset to the next rank.
    """
    return position * (1 + size) / 2, size


@ranker
def sequential(position, size):
    """
    Tie handling function.

    Handle tie ranking using the 'Standard Competition' strategy defined here:
    https://en.wikipedia.org/wiki/Ranking. Tied values are assigned the current
    rank, the next available rank is equal to the next integer.

    Return: A tuple. First item is the rank for tied values ; second item is
            the offset to the next rank.
    """
    return position, 1


class Ranking(BASE):
    """A list of students ordered by their performance to an assessment."""

    # Model definition.
    __tablename__ = 'rankings'
    identifier = Column(Integer(), primary_key=True)
    assessment_id = Column(Integer(), ForeignKey('assessments.identifier'))
    group_id = Column(Integer(), ForeignKey('groups.identifier'))

    assessment = relationship('Assessment')
    group = relationship('Group')
    ranks = relationship('Rank', back_populates='ranking', cascade='all')

    def __init__(self, assessment, group=None, **kwargs) -> None:
        super().__init__()
        self.assessment = assessment
        self.group = group
        self.ranks = [Rank(self, result) for result in assessment.get_results(group)]
        self.start = kwargs.get('start', 1)
        self.handle = kwargs.get('handle', high)

        # Establish ranking.
        self.ranks.sort(key=attrgetter('mark.score'), reverse=kwargs.get('reverse', True))
        for rank, item in self.rank():
            item.position = rank

    def __repr__(self):
        return '<Ranking>'

    def __iter__(self):
        return iter(self.ranks)

    def rank(self):
        """Calculate ranks."""
        index = self.start
        for _, group in groupby(self.ranks, attrgetter('mark.score')):
            group = list(group)
            ranks, offset = self.handle(index, group)
            index += offset
            yield from zip(ranks, group)


class Rank(BASE):
    """Base block in a ranking."""

    # Model definition.
    __tablename__ = 'ranks'
    identifier = Column(Integer(), primary_key=True)
    ranking_id = Column(Integer(), ForeignKey('rankings.identifier'))
    mark_id = Column(Integer(), ForeignKey('marks.identifier'))
    position = Column(Integer(), nullable=False)

    ranking = relationship('Ranking', back_populates='ranks')
    mark = relationship('Mark')

    def __init__(self, ranking, mark, position=None) -> None:
        super().__init__()
        self.ranking = ranking
        self.mark = mark
        self.position = position

    def __repr__(self) -> str:
        return f'<Rank #{self.position}: {self.mark}>'
