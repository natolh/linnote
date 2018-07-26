#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import render_template, request
from flask.views import MethodView
from flask_login import login_required
from linnote.core.user import Group, User, Administrator
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
        return render_template('groups/groups.html', groups=groups)


class GroupRessource(MethodView):
    """Controller for managing a user group ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display a form for creating a new user group."""
        form = GroupForm()
        return render_template('groups/group.html', form=form)

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
        return render_template('users/users.html', users=users)


class UserRessource(MethodView):
    """Controller for managing a user ressource."""

    decorators = [login_required]

    @staticmethod
    def render(**kwargs):
        return render_template('users/user.html', **kwargs)

    @staticmethod
    def load(identifier=None):
        session = WEBSESSION()
        return session.query(User).get(identifier)

    def get(self, identifier=None):
        """Display a form for creating a new user."""
        if identifier:
            user = self.load(identifier)
            form = UserForm(obj=user)
            context = dict(form=form, user=user)

        else:
            form = UserForm()
            context = dict(form=form, user=None)

        return self.render(**context)

    def post(self, identifier=None):
        """Create a new user."""
        session = WEBSESSION()
        form = UserForm()

        if form.validate() and identifier is not None:
            user = self.load(identifier)
            form.populate_obj(user)

        elif form.validate():
            user = User(**form.data)
            profile = Administrator(user=user)
            session.add(profile)

        session.merge(user)
        session.commit()
        return self.get(user.identifier)
