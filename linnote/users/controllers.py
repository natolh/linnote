#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from typing import List
from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import login_required
from linnote.core.user import Group, User, Administrator, Profile
from linnote.core.utils import DATA
from .forms import GroupForm, GroupCreationForm, UserForm
from .logic import load_group


class GroupsController(MethodView):
    """Controls the view of users groups."""

    decorators = [login_required]
    template = 'groups/groups.html'

    def get(self):
        """Display users groups."""
        groups = self.load()
        return self.render(groups=groups)

    @staticmethod
    def load() -> List[Group]:
        """Load groups from storage."""
        data = DATA()
        groups = data.query(Group).all()
        return groups

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class GroupBaseController(MethodView):
    """Common methods for controllers of users group views."""

    decorators = [login_required]
    template = ''

    @staticmethod
    def load(identifier: int) -> Group:
        """Load a group from storage."""
        data = DATA()
        group = data.query(Group).get(identifier)
        return group

    @classmethod
    def render(cls, **kwargs):
        """Render a view."""
        return render_template(cls.template, **kwargs)


class GroupCreationController(GroupBaseController):
    """Controls the view for creating new users groups."""

    template = 'groups/creation.html'

    def get(self):
        """Display a form to gather data needed to create a users group."""
        form = GroupCreationForm()
        return self.render(form=form)

    @staticmethod
    def post():
        """Create a new users group using data of the form."""
        form = GroupCreationForm()
        data = DATA()

        if form.validate() and form.members.data:
            group = load_group(request.files['members'], form.name.data)
            data.add(group)

        elif form.validate():
            group = Group(name=form.name.data)
            data.add(group)

        data.commit()
        return redirect(url_for('users.group', identifier=group.identifier))


class GroupSettingsController(GroupBaseController):
    """Controls the view of group's settings."""

    template = 'groups/group/settings.html'

    def get(self, identifier: int):
        """Display group's settings."""
        group = self.load(identifier)
        form = GroupForm(obj=group)
        return self.render(form=form, group=group)

    def post(self, identifier: int):
        """Modify the group's settings."""
        data = DATA()
        group = self.load(identifier)
        form = GroupForm()
        group.name = form.name.data
        data.commit()
        return self.get(identifier=identifier)


class GroupMembersController(GroupBaseController):
    """Controls the view of group's members."""

    template = 'groups/group/members.html'

    def get(self, identifier):
        """Display groups's members."""
        group = self.load(identifier)
        return self.render(group=group)


class UsersController(MethodView):
    """Controls the view of users."""

    decorators = [login_required]
    template = 'users/users.html'

    def get(self):
        """Display users."""
        users = self.load()
        return self.render(users=users)

    @staticmethod
    def load() -> List[User]:
        """Load users (only administrators) from storage."""
        data = DATA()
        users = data.query(User).join(Profile)
        administrators = users.filter(Profile.role == 'administrator').all()
        return administrators

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class UserBaseController(MethodView):
    """Common methods for controllers of user's view."""

    decorators = [login_required]
    template = 'users/user.html'

    @staticmethod
    def load(identifier: int) -> User:
        """Load a user from storage."""
        data = DATA()
        user = data.query(User).get(identifier)
        return user

    @classmethod
    def render(cls, **kwargs):
        """Render a view."""
        return render_template(cls.template, **kwargs)


class UserCreationController(UserBaseController):
    """Controls the view for creating a user."""

    template = 'users/creation.html'

    def get(self):
        """Display a form for creating a new user."""
        form = UserForm()
        return self.render(form=form, user=None)

    @staticmethod
    def post():
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
    """Controls the view of a user."""

    def get(self, identifier: int):
        """View a user."""
        data = DATA()
        user = self.load(identifier)
        form = UserForm(obj=user)
        form.groups.choices = [(g.identifier, g.name) for g in data.query(Group).all()]
        return self.render(form=form, user=user)

    def post(self, identifier: int):
        """Update user's details."""
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
