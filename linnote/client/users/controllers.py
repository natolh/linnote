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
from linnote.client.utils import session
from .forms import GroupForm, UserForm
from linnote.core.user import Group, User


class GroupCollection(MethodView):
    """Groups collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessments collection."""
        groups = session.query(Group).all()
        return render_template('admin/groups.html', groups=groups)


class GroupRessource(MethodView):
    """Assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessment ressource."""
        form = GroupForm()
        return render_template('admin/group.html', form=form)

    def post(self):
        """Endpoint for assessment ressource."""
        form = GroupForm()
        if form.validate():
            group = Group.load(request.files['students'], form.title.data)
            session.merge(group)
            session.commit()

        return self.get()


class UserCollection(MethodView):
    """Assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessments collection."""
        users = session.query(User).all()
        return render_template('admin/users.html', users=users)


class UserRessource(MethodView):
    """Assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessment ressource."""
        form = UserForm()
        return render_template('admin/user.html', form=form)

    def post(self):
        """Endpoint for assessment ressource."""
        form = UserForm()
        if form.validate():
            user = User(
                form.firstname.data,
                form.lastname.data,
                form.email.data,
                form.password.data)
            session.merge(user)
            session.commit()

        return self.get()