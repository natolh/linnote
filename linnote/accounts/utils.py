#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Login for the application client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from functools import wraps
from flask import redirect, request, url_for
from flask_login import LoginManager
from flask_login import current_user
from linnote.core.user import User
from linnote.core.utils import DATA
from linnote.core.utils.jwt import decode


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


def logged_by_token(function):
    """Token login."""
    @wraps(function)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if token:
            claims = decode(token)
            return function(*args, username=claims['username'], **kwargs)
        return function(*args, username=None, **kwargs)
    return wrapped


# Login manager.
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.session_protection = 'strong'
LOGIN_MANAGER.login_view = 'account.login'


@LOGIN_MANAGER.user_loader
def load_user(identifier):
    """Load user."""
    data = DATA()
    return data.query(User).filter(User.identifier == identifier).one_or_none()
