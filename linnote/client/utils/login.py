#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Login for the application client.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_login import LoginManager
from linnote.core.user import User
from .session import session


# Login manager.
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.session_protection = 'strong'
LOGIN_MANAGER.login_view = 'auth.login'
LOGIN_MANAGER.refresh_view = 'auth.login'

@LOGIN_MANAGER.user_loader
def load_user(identifier):
    """Load user."""
    return session.query(User).filter(User.identifier == identifier).one_or_none()