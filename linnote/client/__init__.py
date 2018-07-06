#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Client for the application (web).

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Flask
from flask_talisman import Talisman
from linnote.accounts.utils import LOGIN_MANAGER
from linnote.core.utils import CSP_POLICY
from linnote.core.utils.configuration import load
from linnote.core.utils import configure as configure_session


def create_app(name=None, config_path='configuration.ini', blueprints=None):
    """
    Create a new application instance.

    - name:         String. The instance name.
    - config_path:  Path-like object. Path to the file holding the
                    configuration.

    Return: A <flask.Flask> object.
    """
    app = Flask(name)

    # Configure app.
    configure_app(app, config_path)
    LOGIN_MANAGER.init_app(app)
    Talisman(app, content_security_policy=CSP_POLICY)

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
    app.template_folder = 'core/templates'
    app.static_folder = 'core/statics'


def register_blueprints(app, blueprints):
    """Register blueprints to the application instance."""
    for blueprint in blueprints:
        blueprint = getattr(blueprint, 'BLUEPRINT')
        app.register_blueprint(blueprint)
