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


def ranker(f):
    @wraps(f)
    def wrapper(position, group):
        size = sum(1 for _ in group)
        rank, offset = f(position, size)
        return repeat(rank, size), offset
    return wrapper


@ranker
def HGH(position, size):
    return position, size


@ranker
def LOW(position, size):
    return position + size - 1, size


# Consider using decimal instead.
@ranker
def AVR(position, size):
    return position * (1 + size) / 2, size


@ranker
def SEQ(position, size):
    return position, 1


class Ranking(object):
    """A ranked sequence of things."""

    def __init__(self, items, key=None, reverse=True, start=1, handle=HGH):
        """
        Create a new ranking.

        - items:    An interable. Items to rank.
        - key:      A callable. When call upon 'item' return a sortable object.
        - label:    A callable. When call upon 'item' return a unique
                    identifier.
        - reverse:  Boolean. If set to True, items are ranked by decreasing
                    order ; if set to False items are ranked by increasing
                    order.
        - start:    Integer. Starting rank.
        - handle:   Callable. A callable to determine rank for tied values and
                    the next rank.

        Return: None.
        """
        super(Ranking, self).__init__()
        self.ranks = [Rank(item, key(item)) for item in items]
        self.key = attrgetter('score')
        self.start = start
        self.handle = handle

        # Establish ranking.
        self.ranks.sort(key=self.key, reverse=reverse)

        for rank, item in self.rank():
            item.position = rank

    def __repr__(self):
        return '<Ranking>'

    def __iter__(self):
        return iter(self.ranks)

    def rank(self):
        """Calculate ranks."""
        index = self.start
        for score, group in groupby(self.ranks, self.key):
            group = list(group)
            ranks, offset = self.handle(index, group)
            index += offset
            yield from zip(ranks, group)


class Rank(object):
    """Ranking item."""

    def __init__(self, item, score, position=None):
        """
        Create a new rank.

        - item:         An object. The item beeing ranked.
        - score:        A sortable value. The score of the person, this value
                        is used to rank.
        - position:     Integer. The student's position in the ranking.

        Return: None.
        """
        super(Rank, self).__init__()
        self.item = item
        self.score = score
        self.position = position

    def __repr__(self):
        return '<Rank #{}: {}>'.format(self.position, self.score)
