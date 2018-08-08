#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import login_required
from linnote.core.user import Group, User, Administrator
from linnote.core.utils import DATA
from .forms import GroupForm, UserForm
from .logic import load_group


class GroupsController(MethodView):
    """Controller for managing user groups collection."""

    decorators = [login_required]
    template = 'groups/groups.html'

    def get(self):
        """Display the collection of user groups."""
        groups = self.load()
        return self.render(groups=groups)

    @staticmethod
    def load():
        """Load groups."""
        data = DATA()
        groups = data.query(Group).all()
        return groups

    @classmethod
    def render(cls, **kwargs):
        """Render groups view."""
        return render_template(cls.template, **kwargs)


class GroupController(MethodView):
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


class UsersController(MethodView):
    """Controller for managing users collection."""

    decorators = [login_required]
    template = 'users/users.html'

    def get(self):
        """Display the collection of users."""
        users = self.load()
        return self.render(users=users)

    @staticmethod
    def load():
        data = DATA()
        users = data.query(User).all()
        return users

    @classmethod
    def render(cls, **kwargs):
        return render_template(cls.template, **kwargs)


class UserBaseController(MethodView):
    """Controller for managing a user ressource."""

    decorators = [login_required]
    template = 'users/user.html'

    @staticmethod
    def load(identifier=None):
        data = DATA()
        user = data.query(User).get(identifier)
        return user

    @classmethod
    def render(cls, **kwargs):
        return render_template(cls.template, **kwargs)


class UserCreationController(UserBaseController):

    template = 'users/creation.html'

    def get(self):
        """Display a form for creating a new user."""
        form = UserForm()
        return self.render(form=form, user=None)

    def post(self):
        """Create a new user."""
        form = UserForm()
        data = DATA()

        if form.validate():
            user = User(**form.data)
            profile = Administrator(identity=user)
            data.add(profile)

        data.merge(user)
        data.commit()

        return redirect(url_for('users.user', identifier=user.identifier))


class UserController(UserBaseController):

    def get(self, identifier):
        user = self.load(identifier)
        form = UserForm(obj=user)
        return self.render(form=form, user=user)

    def post(self, identifier):
        form = UserForm()
        data = DATA()

        if form.validate():
            user = self.load(identifier)
            form.populate_obj(user)

        data.add(user)
        data.commit()

        return self.get(identifier=identifier)
