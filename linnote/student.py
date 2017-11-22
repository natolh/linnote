#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement students.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pandas import read_excel
from linnote.configuration import root


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


class Group(object):
    """A group of students."""

    def __init__(self, students, name=None):
        """Create a new group of students."""
        super(Group, self).__init__()
        self.students = students
        self.name = name

    def __repr__(self):
        return '<Group of students>'

    def __len__(self):
        """Number of students in the group."""
        return len(self.students)

    def __contains__(self, item):
        """Test if a student is in the group."""
        if not isinstance(item, Student):
            raise TypeError

        return item in self.students

    @staticmethod
    def find():
        """
        Discover files containing group definition.

        Return: Generator sequence of path-like objects.
        """
        return root.joinpath("groups").glob("*.xlsx")

    @staticmethod
    def load(file):
        """
        Load a students list from an excel file.

        - file: A path-like object. The path to the file.

        Return: List of 'Student'.
        """
        students = read_excel(file, names=['anonymat']).to_dict('records')
        return [Student(student["anonymat"]) for student in students]
