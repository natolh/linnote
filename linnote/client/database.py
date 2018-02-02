from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from linnote import APP_DIR
from linnote.core.configuration import load

# Create a session factory
config = load(APP_DIR.parent.joinpath('config.ini'))
engine = create_engine(config.get('DATABASE', 'URL'))
session = scoped_session(sessionmaker(bind=engine),
                         _app_ctx_stack.__ident_func__)
