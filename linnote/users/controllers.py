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


class GroupBaseController(MethodView):
    """Controller for managing a user group ressource."""

    decorators = [login_required]

    @staticmethod
    def load(identifier):
        data = DATA()
        group = data.query(Group).get(identifier)
        return group

    @classmethod
    def render(cls, **kwargs):
        return render_template(cls.template, **kwargs)


class GroupCreationController(GroupBaseController):

    template = 'groups/creation.html'

    def get(self):
        form = GroupForm()
        return self.render(form=form)

    def post(self):
        form = GroupForm()
        data = DATA()

        if form.validate() and form.students.data:
            group = load_group(request.files['students'], form.name.data)
            data.merge(group)

        elif form.validate():
            group = Group(name=form.name.data)
            data.add(group)

        data.commit()
        return redirect(url_for('users.group', identifier=group.identifier))


class GroupSettingsController(GroupBaseController):

    template = 'groups/group/settings.html'

    def get(self, identifier):
        """Display a form for creating a new user group."""
        group = self.load(identifier)
        form = GroupForm(obj=group)
        return self.render(form=form, group=group)

    def post(self):
        """Create a new user group."""
        pass


class GroupMembersController(GroupBaseController):

    template = 'groups/group/members.html'

    def get(self, identifier):
        group = self.load(identifier)
        return self.render(group=group)

    def post(self, identifier):
        pass


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
        data = DATA()
        user = self.load(identifier)
        form = UserForm(obj=user)
        form.groups.choices = [(g.identifier, g.name) for g in data.query(Group).all()]
        return self.render(form=form, user=user)

    def post(self, identifier):
        data = DATA()
        form = UserForm()
        form.groups.choices = [(g.identifier, g.name) for g in data.query(Group).all()]

        if form.validate():
            user = self.load(identifier)
            user.first_name = form.firstname.data
            user.last_name = form.lastname.data
            user.email = form.email.data
            user.groups = [data.query(Group).get(id) for id in form.groups.data]

        data.add(user)
        data.commit()

        return self.get(identifier=identifier)
