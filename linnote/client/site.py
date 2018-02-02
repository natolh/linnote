#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Common endpoints.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import redirect, url_for


BLUEPRINT = Blueprint('site', __name__)


@BLUEPRINT.route('/')
def home():
    """Home of the web application."""
    return redirect(url_for('auth.login'))
