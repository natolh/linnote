#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
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
from .configuration import load


# Parent class for every class which objects need to be persist in the
# database.
BASE = declarative_base()


# Create a session factory
CONFIG = load('configuration.ini')
ENGINE = create_engine(CONFIG.get('DATABASE', 'URL'), pool_recycle=20)
SESSION = sessionmaker(bind=ENGINE)


# Create a scoped session for use in the application.
DATA = scoped_session(SESSION, _app_ctx_stack.__ident_func__)


def configure(app) -> None:
    """Ensure the scoped session is closed at the end of the request."""
    app.teardown_appcontext(lambda exception: DATA.remove())
