#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Client for the application (web).

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Flask
from linnote.client.accounts.utils import LOGIN_MANAGER
from linnote.client.utils import STRICT_TRANSPORT
from linnote.core.utils.configuration import load
from linnote.core.utils import configure_session


def create_app(name=None, config_path='configuration.ini', blueprints=None):
    """
    Create a new instance of the application.

    - name:     String. The name of the application instance.
    - config:   A path-like object. Path to the config file for the
                application.

    Return: A new 'flask.Flask' object.
    """
    app = Flask(name)

    # Configure app.
    configure_app(app, config_path)
    LOGIN_MANAGER.init_app(app)
    STRICT_TRANSPORT.init_app(app)

    # Register blueprints to the app.
    if blueprints:
        register_blueprints(app, blueprints)

    # Session.
    configure_session(app)

    return app


def configure_app(app, config_path):
    """Configure an application instance."""
    # Load and set configuration.
    config = load(config_path)
    config = [(k.upper(), v) for (k, v) in config['FLASK'].items()]
    app.config.from_mapping(config)

    # Fix configuration for some special parameters.
    app.template_folder = app.config['TEMPLATE_FOLDER']
    app.static_folder = app.config['STATIC_FOLDER']


def register_blueprints(app, blueprints):
    """Register blueprints to the application instance."""
    for blueprint in blueprints:
        blueprint = getattr(blueprint, 'BLUEPRINT')
        app.register_blueprint(blueprint)
