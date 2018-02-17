#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Controllers for the 'users' app module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import render_template
from flask_login import login_required
from linnote.client.utils import session
from linnote.client.utils.controller import Controller
from .forms import UserForm
from linnote.core.user import User


class UserCollection(Controller):
    """Assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessments collection."""
        users = session.query(User).all()
        return render_template('admin/users.html', users=users)


class UserRessource(Controller):
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