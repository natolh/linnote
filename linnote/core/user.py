#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement users.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pandas import read_excel
from sqlalchemy import Column, Table
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from .utils.database import BASE


class User(BASE):
    """Someone that use the application."""

    # Model definition.
    __tablename__ = 'users'
    identifier = Column(Integer(), primary_key=True)
    firstname = Column(String(250))
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True, index=True)
    password_hash = Column(Text())
    is_verified = Column(Boolean(), default=False)

    profile = relationship('Profile', back_populates='user',
                           uselist=False, cascade='all')

    def __init__(self, firstname, lastname, email, **kwargs) -> None:
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

        if kwargs.get('password'):
            self.set_password_hash(kwargs.get('password'))

    def __repr__(self) -> str:
        return f'<User {self.identifier}: {self.fullname}>'

    def __str__(self) -> str:
        return self.fullname

    @hybrid_property
    def username(self):
        """Alias for 'self.email'."""
        return self.email

    @hybrid_property
    def fullname(self) -> str:
        """User's fullname (concatenation of first and last names)."""
        return f'{self.firstname} {self.lastname}'

    def get_id(self) -> str:
        """
        Return the user identifier as a string for login.

        This method is required to use flask_login extension.
        """
        return str(self.identifier)

    def set_password_hash(self, password: str) -> str:
        """Set user's password."""
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def is_authentic(self, password: str) -> bool:
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


class Profile(BASE):
    """User's details not related to his identity in the application."""

    # Model definition.
    __tablename__ = 'profiles'
    identifier = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.identifier'))
    role = Column(String(250), nullable=False)
    user = relationship('User', back_populates='profile', uselist=False)

    __mapper_args__ = {'polymorphic_on': role, 'polymorphic_identity': '*'}


class Administrator(Profile):
    """Someone that loves to keep students busy."""

    # Model definition.
    __tablename__ = 'profiles__administrators'
    __mapper_args__ = {'polymorphic_identity': 'administrator'}
    identifier = Column(Integer(),
                        ForeignKey('profiles.identifier'),
                        primary_key=True)
    is_superuser = Column(Boolean(),
                          default=False)


class Student(Profile):
    """Someone seeking to learn about life, the universe and everything."""

    # Model definition.
    __tablename__ = 'profiles__students'
    __mapper_args__ = {'polymorphic_identity': 'student'}
    identifier = Column(Integer(),
                        ForeignKey('profiles.identifier'), primary_key=True)
    aid = Column(Integer())
    groups = relationship(
                'Group',
                secondary='students_groups',
                back_populates='students')
    results = relationship(
                'Mark',
                back_populates='student')

    def __repr__(self) -> str:
        return f'<Student {self.identifier}>'

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


STUDENTS_GROUPS = Table(
    'students_groups',
    BASE.metadata,
    Column('group', Integer, ForeignKey('groups.identifier')),
    Column('student', Integer, ForeignKey('profiles__students.identifier'))
)
