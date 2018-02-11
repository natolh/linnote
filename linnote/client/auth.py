#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Authentification endpoints for the web client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from linnote.core.user import User
from .utils import session
from .forms import LoginForm


BLUEPRINT = Blueprint('auth', __name__)


@BLUEPRINT.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint for the application."""
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))

    if request.method == 'POST' and form.validate():
        user = session.query(User).filter(User.username == form.identifier.data).one_or_none()

        if user and user.is_authentic(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('admin.home'))

    return render_template('authentification/login.html', form=form)

@BLUEPRINT.route('/logout')
def logout():
    """Logout endpoint for the application."""
    logout_user()
    return redirect(url_for('auth.login'))
