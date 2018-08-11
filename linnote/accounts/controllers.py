#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'accounts' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from functools import wraps
from flask import redirect, render_template, url_for, request
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from jwt import decode
from linnote.core.user import User
from linnote.core.utils import DATA
from .forms import LoginForm, PasswordForm, ProfileForm


def skip_if_authenticated(function):
    """
    Redirect user to homepage if authentificated.

    This function purpose is to be used as a decorator on the login page to
    avoid the hassle of login a user that is already authentificated.
    """
    @wraps(function)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('assessments.assessment_creation'))
        return function(*args, **kwargs)
    return wrapped


class Login(MethodView):
    """Controller for managing user login task."""

    decorators = [skip_if_authenticated]

    def get(self):
        """
        Display login formular or allow for login using a token.
        """
        token = request.args.get('token', None)
        if token:
            return self.login_from_token(token)

        form = LoginForm()
        return render_template('authentification/login.html', form=form)

    def post(self):
        """Process the login formular, login the user, redirect to his desk."""
        return self.login_from_formular()

    @staticmethod
    def login_from_formular():
        form = LoginForm()
        data = DATA()

        if form.validate():
            users = data.query(User)
            user = users.filter_by(username=form.identifier.data).one_or_none()

            if user and user.is_authentic(form.password.data):
                login_user(user)
                return redirect(url_for('assessments.assessments'))

        return self.get()


    @staticmethod
    def login_from_token(token):
        data = DATA()
        claims = decode(token, 'secret')
        users = data.query(User)
        user = users.filter_by(username=claims['username']).one_or_none()

        if user:
            login_user(user)
            return redirect(url_for('assessments.assessments'))


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
        return render_template('password.html', form=form)

    def post(self):
        """Process the password modification formular."""
        form = PasswordForm()
        if all([form.validate(),
                current_user.is_authentic(form.old_password.data),
                form.password.data == form.password_confirm.data]):
            current_user.set_password_hash(form.password.data)
            DATA.commit()

        return self.get()


class Profile(MethodView):
    """Controller for managing the user's profile."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Get the profile modification formular."""
        form = ProfileForm(obj=current_user)
        return render_template('profile.html', form=form)

    def post(self):
        """Process the profile modification formular."""
        form = ProfileForm()
        if form.validate():
            form.populate_obj(current_user)
            DATA.commit()
        return self.get()
