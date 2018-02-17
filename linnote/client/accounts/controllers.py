#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Controllers for the 'accounts' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from linnote.client.utils import session
from linnote.core.user import User
from .forms import LoginForm, PasswordForm, ProfileForm


class Login(MethodView):
    """Controller for managing user login task."""

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
                return redirect(url_for('assessments.assessments'))

        return self.get()


class Logout(MethodView):
    """Controller for managing user logout task."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Logout the user, redirect to home."""
        logout_user()
        return redirect(url_for('account.login'))


class Password(MethodView):
    """Controller for managing the user's account password."""

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


class Profile(MethodView):
    """Controller for managing the user's profile."""

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
