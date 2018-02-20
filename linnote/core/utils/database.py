#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement database object.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from linnote import APP_DIR
from .configuration import load


# Parent class for every class which objects need to be persist in the
# database.
Base = declarative_base()

# Create a session factory
CONFIG = load(APP_DIR.parent.joinpath('configuration.ini'))
ENGINE = create_engine(CONFIG.get('DATABASE', 'URL'), pool_recycle=280)
Session = sessionmaker(bind=ENGINE)
