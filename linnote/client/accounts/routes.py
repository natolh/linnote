#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Accounts routes.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Login, Logout, Profile, Password


login_view = Login.as_view('login')
logout_view = Logout.as_view('logout')
profile_view = Profile.as_view('profile')
password_view = Password.as_view('password')


ROUTES = Blueprint('account', __name__, url_prefix='/account')
ROUTES.add_url_rule('/login', view_func=login_view)
ROUTES.add_url_rule('/logout', view_func=logout_view)
ROUTES.add_url_rule('/profile', view_func=profile_view)
ROUTES.add_url_rule('/password', view_func=password_view)