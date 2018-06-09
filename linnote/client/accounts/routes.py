#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes for the 'accounts' application module..

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Login, Logout, Profile, Password


# Build controllers functions.
LOGIN = Login.as_view('login')
LOGOUT = Logout.as_view('logout')
PROFILE = Profile.as_view('profile')
PASSWORD = Password.as_view('password')


# Register routes to controllers.
ROUTES = Blueprint('account', __name__, url_prefix='/account')


ROUTES.add_url_rule('/login', view_func=LOGIN)
ROUTES.add_url_rule('/logout', view_func=LOGOUT)
ROUTES.add_url_rule('/profile', view_func=PROFILE)
ROUTES.add_url_rule('/password', view_func=PASSWORD)
