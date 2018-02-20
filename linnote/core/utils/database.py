#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement database related tools.

Define a 'Base' class that sould be inherited by every class to persist in the
database. Define a 'web_session' object to be used in the client to perform
actions on the database. Define a 'configure' function for binding the
'web_session' to the client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from linnote import APP_DIR
from .configuration import load


# Parent class for every class which objects need to be persist in the
# database.
BASE = declarative_base()


# Create a session factory
CONFIG = load(APP_DIR.parent.joinpath('configuration.ini'))
ENGINE = create_engine(CONFIG.get('DATABASE', 'URL'), pool_recycle=280)
Session = sessionmaker(bind=ENGINE)


# Create a scoped session for use in the application.
websession = scoped_session(Session, _app_ctx_stack.__ident_func__)


def configure(app):
    """
    Configure the flask app to use the session.

    Place a reference to the scoped_session in a 'session' attribute of the
    application. Ensure that the 'session' is correctly removed at the teardown
    of each request.

    Return: None.
    """
    app.session = websession
    app.teardown_appcontext(lambda *args, **kwargs: app.session.remove())
