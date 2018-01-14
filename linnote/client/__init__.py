#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Web client for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pathlib import Path
from flask import Flask
from linnote import APP_DIR
from linnote.configuration import load
from linnote.client.controllers import site
from linnote.client.api import API


def create_app(name=None, config_path='config.ini'):
    """
    Create a new instance of the application.

    - name:     String. The name of the application instance.
    - config:   A path-like object. Path to the config file for the application.

    Return: A new 'flask.Flask' object.
    """
    app = Flask(name)
    configure_app(app, config_path)
    app.register_blueprint(site)
    app.register_blueprint(API)
    return app

def configure_app(app, config_path):
    """Configure an application instance."""
    # Locate configuration file.
    config_path = Path(config_path)
    if not config_path.is_absolute():
        APP_DIR.joinpath(config_path)

    # Load and set configuration.
    config = load(config_path)
    config = [(k.upper(), v) for (k, v) in config['FLASK'].items()]
    app.config.from_mapping(config)

    # Fix configuration for some special parameters.
    app.template_folder = app.config['TEMPLATE_FOLDER']
    app.static_folder = app.config['STATIC_FOLDER']
