#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Utils for Flask.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from linnote import APP_DIR
from linnote.core.utils.configuration import load


# Session factory.
config = load(APP_DIR.parent.joinpath('configuration.ini'))
engine = create_engine(config.get('DATABASE', 'URL'), pool_recycle=280)
session = scoped_session(sessionmaker(bind=engine),
                         _app_ctx_stack.__ident_func__)


def configure_session(app):

    app.session = session

    @app.teardown_appcontext
    def remove(*args, **kwargs):
        app.session.remove()
