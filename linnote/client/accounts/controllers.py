#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Accounts controllers.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from linnote.client.utils import session
from linnote.client.utils.controller import Controller
from linnote.core.user import User
from .forms import LoginForm, PasswordForm, ProfileForm


class Login(Controller):
    """Login endpoint. This endpoint support the login mechanism."""

    @staticmethod
    def get():
        """Get the login formular or skip is user is already authentificated."""
        if current_user.is_authenticated:
            return redirect(url_for('admin.home'))

        form = LoginForm()
        return render_template('account/authentification/login.html', form=form)

    def post(self):
        """Process the login formular, login the user, redirect to his desk."""
        form = LoginForm()
        if form.validate():
            user = session.query(User).filter(User.username == form.identifier.data).one_or_none()

            if user and user.is_authentic(form.password.data):
                login_user(user)
                return redirect(url_for('admin.home'))

        return self.get()


class Logout(Controller):
    """Logout endpoint. This endpoint support the logout mechanism."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Logout the user, redirect to home."""
        logout_user()
        return redirect(url_for('account.login'))


class Password(Controller):
    """
    User's password endpoint.

    This endpoint is design to allow the user to modify his account password.
    It is impossible to vizualize the actual account password as they're not
    stored in plain text.
    """

    decorators = [login_required]

    @staticmethod
    def get():
        """Get the password modification formular."""
        form = PasswordForm()
        return render_template('account/password.html', form=form)

    def post(self):
        """Process the password modification formular."""
        form = PasswordForm()
        if all([form.validate(),
                current_user.is_authentic(form.old_password.data),
                form.password.data == form.password_confirm.data]):
            current_user.set_password(form.password.data)
            session.commit()

        return self.get()

class Profile(Controller):
    """
    User's profile endpoint.

    This endpoint is design to allow the user to view and modify some of his
    account property. Currently this properties are available : user's
    firstname, lastname and email.
    """

    decorators = [login_required]

    @staticmethod
    def get():
        """Get the profile modification formular."""
        form = ProfileForm(obj=current_user)
        return render_template('account/profile.html', form=form)

    def post(self):
        """Process the profile modification formular."""
        form = ProfileForm()
        if form.validate():
            form.populate_obj(current_user)
            session.commit()

        return self.get()
