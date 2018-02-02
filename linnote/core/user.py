#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement users.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from .database import Base


class User(Base):
    """A user of the application."""

    __tablename__ = 'users'

    identifier = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True, index=True)
    email = Column(String(250), nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=True)
    is_verified = Column(Boolean)
    is_active = Column(Boolean)

    def __repr__(self):
        return '<User: {}>'.format(self.name)

    def get_id(self):
        """
        Return the user identifier as a string for login.

        This method is required for the use of flask_login extension.
        """
        return str(self.identifier)

    def set_password(self, password):
        """
        Set the user password.

        - password: String. The password for the user.

        Return: String. The password hash.
        """
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def is_authentic(self, password):
        """Check if the provided password match the user registred password."""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def is_authenticated():
        """Boolean showing if the current user is authenticated or not."""
        return True

    def is_anonymous(self):
        """Boolean showing if the current user is anonymous or not."""
        return not self.is_authenticated()
