#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module allow the user to manage his account.

The user can edit his profile, change his password, reset his account, and
obviously login/logout from the application.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import AccountLoginController, AccountLogoutController
from .controllers import AccountProfileController, AccountPasswordController
from .controllers import AccountResetController


# Create the module.
BLUEPRINT = Blueprint('account', __name__)
BLUEPRINT.url_prefix = '/account'
BLUEPRINT.template_folder = 'templates'
BLUEPRINT.static_folder = 'statics'

# Build views' controllers.
LOGIN = AccountLoginController.as_view('login')
LOGOUT = AccountLogoutController.as_view('logout')
PROFILE = AccountProfileController.as_view('profile')
PASSWORD = AccountPasswordController.as_view('password')
RESET = AccountResetController.as_view('reset')

# Register views' controllers routes.
BLUEPRINT.add_url_rule('/login', view_func=LOGIN)
BLUEPRINT.add_url_rule('/logout', view_func=LOGOUT)
BLUEPRINT.add_url_rule('/profile', view_func=PROFILE)
BLUEPRINT.add_url_rule('/password', view_func=PASSWORD)
BLUEPRINT.add_url_rule('/reset', view_func=RESET)
