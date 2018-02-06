#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement student and students groups.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from os import remove
from pickle import dump, load
from pandas import read_excel
from linnote import APP_DIR


STORAGE = APP_DIR.parent.joinpath('storage', 'groups')


class Student(object): # pylint: disable=R0903
    """Someone seeking to learn about life, the universe and everything."""

    def __init__(self, identifier):
        """
        Initialize a new student.

        - identifier:   An integer. A unique, anonymous, identifier for the
                        student to use during assessments.

        Return: None.
        """
        super().__init__()
        self.identifier = identifier

    def __repr__(self):
        return '<Student #{}>'.format(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.identifier)


class Group(object):
    """A group of students."""

    def __init__(self, students, name=None):
        """
        Initialize a new group of students.

        - students: List of 'Student' objects. Members of the group.
        - name:     String. The name of the group.

        Return: None.
        """
        super().__init__()
        self.students = students
        self.name = name

    def __repr__(self):
        return '<Group of students: {}>'.format(self.name)

    def __len__(self):
        return len(self.students)

    def __iter__(self):
        return iter(self.students)

    def __contains__(self, item):
        if not isinstance(item, Student):
            raise TypeError

        return item in self.students

    @staticmethod
    def fetch(filename=None):
        if not filename:
            return STORAGE.glob('*')

        group = STORAGE.joinpath(filename).open('rb')
        return load(group)

    @staticmethod
    def load(file, name=None):
        """
        Load a student group from an excel file.

        - file: A path-like object. The path to the file.
        - name: String. The group's name.

        Return: A 'Group' object.
        """
        students = read_excel(file, names=['identifier']).to_dict('records')
        students = [Student(student["identifier"]) for student in students]
        return Group(students=students, name=name)

    def save(self, filename):
        dump(self, STORAGE.joinpath(filename).open('wb'), -1)

    def delete(self, filename):
        remove(STORAGE.joinpath(filename))
