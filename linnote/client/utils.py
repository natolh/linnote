#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Utils for Flask.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import _app_ctx_stack
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from linnote import APP_DIR
from linnote.core.configuration import load
from linnote.core.user import User


# Session factory.
config = load(APP_DIR.parent.joinpath('config.ini'))
engine = create_engine(config.get('DATABASE', 'URL'))
session = scoped_session(sessionmaker(bind=engine),
                         _app_ctx_stack.__ident_func__)


# Login manager.
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.session_protection = 'strong'
LOGIN_MANAGER.login_view = 'auth.login'
LOGIN_MANAGER.refresh_view = 'auth.login'

@LOGIN_MANAGER.user_loader
def load_user(identifier):
    """Load user."""
    return session.query(User).filter(User.identifier == identifier).one_or_none()
