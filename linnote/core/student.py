#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement student and students groups.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pandas import read_excel
from sqlalchemy import Column, Table
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .utils.database import Base


class Student(Base): # pylint: disable=R0903
    """
    Someone seeking to learn about life, the universe and everything.

    - identifier:   An integer. A unique, anonymous, identifier for the
                    student to use during assessments.
    """

    __tablename__ = 'students'
    identifier = Column(Integer, primary_key=True)
    groups = relationship('Group', secondary='students_groups', back_populates='students')

    def __repr__(self):
        return '<Student #{}>'.format(self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.identifier)


class Group(Base):
    """
    A group of students.

    - name:     String. The name of the group.
    - students: List of 'Student' objects. Members of the group.
    """

    __tablename__ = 'groups'

    identifier = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True, index=True)
    students = relationship('Student', secondary='students_groups', back_populates='groups')

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
    def load(file, name=None):
        """
        Load a student group from an excel file.

        - file: A path-like object. The path to the file.
        - name: String. The group's name.

        Return: A 'Group' object.
        """
        group = Group(name=name)

        students = read_excel(file, names=['identifier']).to_dict('records')
        for student in students:
            student = Student(identifier=int(student['identifier']))
            group.students.append(student)

        return group


STUDENTS_GROUPS = Table(
    'students_groups',
    Base.metadata,
    Column('group', Integer, ForeignKey('groups.identifier')),
    Column('student', Integer, ForeignKey('students.identifier'))
)
