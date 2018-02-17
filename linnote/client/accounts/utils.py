#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Login for the application client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_login import LoginManager
from linnote.core.user import User
from linnote.client.utils.session import session


# Login manager.
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.session_protection = 'strong'
LOGIN_MANAGER.login_view = 'account.login'


@LOGIN_MANAGER.user_loader
def load_user(identifier):
    """Load user."""
    return session.query(User).filter(User.identifier == identifier).one_or_none()
