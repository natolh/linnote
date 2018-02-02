#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement database object.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
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
config = load(APP_DIR.parent.joinpath('config.ini'))
engine = create_engine(config.get('DATABASE', 'URL'))
Session = sessionmaker(bind=engine)
