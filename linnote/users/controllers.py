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
from linnote.core.utils import DATA
from .forms import GroupForm, UserForm
from .logic import load_group


class GroupCollection(MethodView):
    """Controller for managing user groups collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the collection of user groups."""
        groups = DATA.query(Group).all()
        return render_template('groups/groups.html', groups=groups)


class GroupRessource(MethodView):
    """Controller for managing a user group ressource."""

    decorators = [login_required]
    template = 'groups/group.html'

    def get(self):
        """Display a form for creating a new user group."""
        form = GroupForm()
        return self.render(form=form)

    def post(self):
        """Create a new user group."""
        form = GroupForm()
        data = DATA()

        if form.validate() and form.students.data:
            group = load_group(request.files['students'], form.title.data)
            data.merge(group)

        elif form.validate():
            group = Group(name=form.title.data)
            data.add(group)

        data.commit()
        return self.get()

    @classmethod
    def render(cls, **kwargs):
        return render_template(cls.template, **kwargs)

class UserCollection(MethodView):
    """Controller for managing users collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the collection of users."""
        users = DATA.query(User).all()
        return render_template('users/users.html', users=users)


class UserRessource(MethodView):
    """Controller for managing a user ressource."""

    decorators = [login_required]

    @staticmethod
    def render(**kwargs):
        return render_template('users/user.html', **kwargs)

    @staticmethod
    def load(identifier=None):
        return DATA.query(User).get(identifier)

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
        form = UserForm()

        if form.validate() and identifier is not None:
            user = self.load(identifier)
            form.populate_obj(user)

        elif form.validate():
            user = User(**form.data)
            profile = Administrator(identity=user)
            DATA.add(profile)

        DATA.merge(user)
        DATA.commit()
        return self.get(user.identifier)
