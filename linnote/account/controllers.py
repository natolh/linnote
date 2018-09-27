#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'account' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from linnote.core.user import User
from linnote.core.utils import DATA
from .forms import LoginForm, PasswordChangeForm, PasswordForm, ProfileForm
from .utils import skip_if_authenticated, logged_by_token


class AccountLoginController(MethodView):
    """Controller for managing user login task."""

    decorators = [skip_if_authenticated]
    template = 'account/authentification/login.html'

    def get(self):
        """
        Display login formular or allow for login using a token.
        """
        form = LoginForm()
        return self.render(form=form)

    def post(self):
        """Process the login formular, login the user, redirect to his desk."""
        form = LoginForm()
        data = DATA()

        if form.validate():
            users = data.query(User)
            user = users.filter_by(username=form.identifier.data).one_or_none()

            if user and user.is_authentic(form.password.data):
                login_user(user)
                return redirect(url_for('assessments.assessments'))

        return self.render(form=form)

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class AccountLogoutController(MethodView):
    """Controller for managing user logout task."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Logout the user, redirect to home."""
        logout_user()
        return redirect(url_for('account.login'))


class AccountProfileController(MethodView):
    """
    Control user's account profile view.

    Profile view expose user's identity data as well as extra user's related
    data known as profile.
    """

    decorators = [login_required]
    template = 'account/profile.html'

    def get(self):
        """Display the profile."""
        form = ProfileForm(obj=current_user)
        return self.render(form=form)

    def post(self):
        """Process the profile modification formular."""
        data = DATA()
        form = ProfileForm()
        if form.validate():
            form.populate_obj(current_user)
            data.commit()
        return self.get()

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class AccountPasswordController(MethodView):
    """Controller for managing the user's account password."""

    decorators = [login_required]
    template = 'account/password.html'

    def get(self):
        """Get the password modification formular."""
        form = PasswordChangeForm()
        return self.render(form=form)

    def post(self):
        """Process the password modification formular."""
        data = DATA()
        form = PasswordChangeForm()

        valid_form = form.validate()
        authentic_user = current_user.is_authentic(form.old_password.data)

        if valid_form and authentic_user:
            current_user.set_password_hash(form.password.data)
            data.commit()

        return self.render(form=form)

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class AccountResetController(MethodView):
    """Controller for resetting the user's account password."""

    template = 'account/authentification/reset.html'

    def get(self):
        """Build user's account password reset view."""
        form = PasswordForm()
        return self.render(form=form)

    @logged_by_token
    def post(self, username):
        """Reset user's account password."""
        data = DATA()
        user = data.query(User).filter_by(username=username).one_or_none()
        form = PasswordForm()

        if form.validate() and user:
            user.set_password_hash(form.password.data)
            data.commit()
            return redirect(url_for('assessments.assessments'))
        return self.render(form=form)

    @staticmethod
    def load(username):
        """Load user from storage."""
        data = DATA()
        user = data.query(User).get(username)
        return user

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)
