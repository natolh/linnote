#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement students.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


class Student(object):
    """Represent a student."""

    def __init__(self, identifier):
        super(Student, self).__init__()
        self.identifier = identifier

    def __repr__(self):
        return '<Student #{}>'.format(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.identifier < other.identifier

    def __le__(self, other):
        return self.identifier <= other.identifier

    def __gt__(self, other):
        return self.identifier > other.identifier

    def __ge__(self, other):
        return self.identifier >= other.identifier

    def __hash__(self):
        return hash(self.identifier)
