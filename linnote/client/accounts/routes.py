#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Accounts routes.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Login, Logout, Profile, Password


ROUTES = Blueprint('account', __name__, url_prefix='/account')


Login.register_to(ROUTES)
Logout.register_to(ROUTES)
Profile.register_to(ROUTES)
Password.register_to(ROUTES)
