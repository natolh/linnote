#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implement users.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from time import time
from typing import Iterator, List
from sqlalchemy import Column, Table
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import BASE
from .utils.jwt import encode


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

    profile = relationship(
        'Profile', back_populates='identity', uselist=False, cascade='all')
    groups = relationship(
        'Group', secondary='users_groups', back_populates='members')

    def __init__(self, firstname, lastname, email, password=None) -> None:
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        if password:
            self.set_password_hash(password)

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

    def access_token(self, duration=3600):
        """
        Create a temporary JWT access token.

        Currently used only for initializing account's password or recovering
        it.
        """
        token = dict()
        token['issuer'] = 'linnote'
        token['iat'] = time()
        token['exp'] = token['iat'] + duration
        token['username'] = self.username
        return encode(token)


class Profile(BASE):
    """User's details not related to his identity in the application."""

    # Model definition.
    __tablename__ = 'profiles'
    identifier = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.identifier'))
    role = Column(String(250), nullable=False)
    identity = relationship('User', back_populates='profile', uselist=False)

    __mapper_args__ = {
        'polymorphic_on': role, 'with_polymorphic': '*'}


class Administrator(Profile):
    """Someone that loves to keep students busy."""

    # Model definition.
    __tablename__ = 'profiles__administrators'
    __mapper_args__ = {'polymorphic_identity': 'administrator'}
    identifier = Column(Integer(), ForeignKey('profiles.identifier'),
                        primary_key=True)
    is_superuser = Column(Boolean(), default=False)


class Student(Profile):
    """Someone seeking to learn about life, the universe and everything."""

    # Model definition.
    __tablename__ = 'profiles__students'
    __mapper_args__ = {'polymorphic_identity': 'student'}
    identifier = Column(Integer(),
                        ForeignKey('profiles.identifier'), primary_key=True)
    aid = Column(Integer())
    results = relationship('Mark', back_populates='student')

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
    A bunch of users that are somewhat related.

    The 'members' attribute that stores the collection of group's users is a
    'list' to ensure compatibility with SQLAlchemy. But Group methods will
    behave like if it is a set to ensure that no duplicate is present.
    """

    # SQLAlchemy model definition.
    __tablename__ = 'groups'
    identifier = Column(Integer(), primary_key=True)
    name = Column(String(250), nullable=False, unique=True, index=True)
    members = relationship(
        'User', secondary='users_groups', back_populates='groups')

    # Object methods.
    def __init__(self, name: str = None, members: List[User] = None) -> None:
        super().__init__()
        self.name = name
        self.members = members if members else list()

    def __repr__(self) -> str:
        return f'<User Group: {self.name}>'

    def __str__(self) -> str:
        return self.name if self.name else ''

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self) -> Iterator:
        return iter(self.members)

    def __contains__(self, value) -> bool:
        return value in self.members

    def append(self, user: User):
        """
        Add a new user to group's members.

        If the user is already present in the list, it will not be added a
        second time.
        """
        if not user in set(self.members):
            self.members.append(user)

    def extend(self, users: List[User]):
        """
        Add a list of users to group's members.

        If a user is already present in the list, it will not be added a
        second time.
        """
        actual_members = set(self.members)
        candidates = set(users)
        self.members.extend(candidates - actual_members)

    def remove(self, user: User):
        """Remove a user from group's members."""
        self.members.remove(user)

    def pop(self, user: User) -> User:
        """
        Remove a user from group's members.

        The removed user is then returned.
        """
        return self.members.pop(user)

    def clear(self):
        """Remove all group's members."""
        self.members.clear()


USERS_GROUPS = Table(
    'users_groups',
    BASE.metadata,
    Column('group', Integer, ForeignKey('groups.identifier')),
    Column('user', Integer, ForeignKey('users.identifier'))
)
