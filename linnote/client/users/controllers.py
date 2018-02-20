#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Controllers for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import render_template, request
from flask.views import MethodView
from flask_login import login_required
from linnote.core.user import Group, User
from linnote.core.utils import WEBSESSION
from .forms import GroupForm, UserForm


class GroupCollection(MethodView):
    """Controller for managing user groups collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the collection of user groups."""
        session = WEBSESSION()
        groups = session.query(Group).all()
        return render_template('users/groups/collection.html', groups=groups)


class GroupRessource(MethodView):
    """Controller for managing a user group ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display a form for creating a new user group."""
        form = GroupForm()
        return render_template('users/groups/ressource.html', form=form)

    def post(self):
        """Create a new user group."""
        session = WEBSESSION()
        form = GroupForm()
        if form.validate():
            group = Group.load(request.files['students'], form.title.data)
            session.merge(group)
            session.commit()

        return self.get()


class UserCollection(MethodView):
    """Controller for managing users collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the collection of users."""
        session = WEBSESSION()
        users = session.query(User).all()
        return render_template('users/collection.html', users=users)


class UserRessource(MethodView):
    """Controller for managing a user ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display a form for creating a new user."""
        form = UserForm()
        return render_template('users/ressource.html', form=form)

    def post(self):
        """Create a new user."""
        session = WEBSESSION()
        form = UserForm()
        if form.validate():
            user = User(
                form.firstname.data,
                form.lastname.data,
                form.email.data,
                password=form.password.data)
            session.merge(user)
            session.commit()

        return self.get()
