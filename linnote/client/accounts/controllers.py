#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Accounts controllers.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

__all__ = ['Login', 'Logout', 'Profile', 'Password']

from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from linnote.client.utils import session
from linnote.core.user import User
from .forms import LoginForm, PasswordForm, ProfileForm


class Login(MethodView):

    @staticmethod
    def get():
        if current_user.is_authenticated:
            return redirect(url_for('admin.home'))

        form = LoginForm()
        return render_template('account/authentification/login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate():
            user = session.query(User).filter(User.username == form.identifier.data).one_or_none()

            if user and user.is_authentic(form.password.data):
                login_user(user)
                return redirect(request.args.get('next') or url_for('admin.home'))

        return self.get()


class Logout(MethodView):

    decorators = [login_required]

    @staticmethod
    def get():
        logout_user()
        return redirect(url_for('account.login'))


class Password(MethodView):

    decorators = [login_required]

    @staticmethod
    def get():
        form = PasswordForm()
        return render_template('account/password.html', form=form)

    def post(self):
        form = PasswordForm()
        if all([form.validate(),
                current_user.is_authentic(form.old_password.data),
                form.password.data == form.password_confirm.data]):
            current_user.set_password(form.password.data)
            session.commit()

        return self.get()

class Profile(MethodView):

    decorators = [login_required]

    @staticmethod
    def get():
        form = ProfileForm(obj=current_user)
        return render_template('account/profile.html', form=form)

    def post(self):
        form = ProfileForm()
        if form.validate():
            form.populate_obj(current_user)
            session.commit()

        return self.get()
