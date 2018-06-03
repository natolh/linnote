#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement users.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pandas import read_excel
from sqlalchemy import Boolean, Column, Integer, String, Table, Text, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from .utils.database import BASE


class User(BASE):
    """A user of the application."""

    __tablename__ = 'users'

    identifier = Column(Integer, primary_key=True)
    firstname = Column(String(250))
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    def __init__(self, firstname, lastname, email, **kwargs) -> None:
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.is_staff = kwargs.get('is_staff', False)
        self.is_superuser = kwargs.get('is_superuser', False)

        if kwargs.get('password'):
            self.set_password(kwargs.get('password'))

    def __repr__(self) -> str:
        return '<User #{}: {}>'.format(self.identifier, self.fullname)

    def __str__(self) -> str:
        return '{}'.format(self.fullname)

    @hybrid_property
    def username(self):
        """Alias for 'self.email'."""
        return self.email

    @hybrid_property
    def fullname(self):
        """User's fullname (concatenation of first and last names)."""
        return '{} {}'.format(self.firstname, self.lastname)

    def get_id(self):
        """
        Return the user identifier as a string for login.

        This method is required for the use of flask_login extension.
        """
        return str(self.identifier)

    def set_password(self, password) -> str:
        """
        Set the user password.

        - password: String. The password for the user.

        Return: String. The password hash.
        """
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def is_authentic(self, password) -> bool:
        """Check if the provided password match the user registred password."""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def is_authenticated() -> bool:
        """Boolean showing if the current user is authenticated or not."""
        return True

    def is_anonymous(self) -> bool:
        """Boolean showing if the current user is anonymous or not."""
        return not self.is_authenticated()

    @staticmethod
    def is_active() -> bool:
        """Boolean showing if the current user account is active or not."""
        return True

    def update(self, data):
        """Update user's attribute using dict values."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Student(BASE):
    """
    Someone seeking to learn about life, the universe and everything.

    - identifier:   An integer. A unique, anonymous, identifier for the
                    student to use during assessments.
    """

    __tablename__ = 'students'
    identifier = Column(Integer, primary_key=True)
    groups = relationship('Group', secondary='students_groups', back_populates='students')

    results = relationship('Mark', back_populates='student')

    def __init__(self, identifier=None):
        super().__init__()
        self.identifier = identifier

    def __repr__(self) -> str:
        return '<Student #{}>'.format(self.identifier)

    def __eq__(self, other) -> bool:
        if isinstance(other, Student):
            return self.identifier == other.identifier

        return NotImplemented

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.identifier)


class Group(BASE):
    """
    A group of students.

    - name:     String. The name of the group.
    - students: List of 'Student' objects. Members of the group.
    """

    __tablename__ = 'groups'
    identifier = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True, index=True)
    students = relationship('Student', secondary='students_groups', back_populates='groups')

    def __repr__(self) -> str:
        return '<Group of students: {}>'.format(self.name)

    def __len__(self) -> int:
        return len(self.students)

    def __iter__(self):
        return iter(self.students)

    def __contains__(self, item) -> bool:
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
    BASE.metadata,
    Column('group', Integer, ForeignKey('groups.identifier')),
    Column('student', Integer, ForeignKey('students.identifier'))
)
