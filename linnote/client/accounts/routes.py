#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Accounts routes.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

__all__ = ['ROUTES']

from flask import Blueprint
from .controllers import Login, Logout, Profile, Password


ROUTES = Blueprint('account', __name__, url_prefix='/account')


ROUTES.add_url_rule('/login', view_func=Login.as_view('login'))
ROUTES.add_url_rule('/logout', view_func=Logout.as_view('logout'))
ROUTES.add_url_rule('/profile', view_func=Profile.as_view('profile'))
ROUTES.add_url_rule('/password', view_func=Password.as_view('password'))
