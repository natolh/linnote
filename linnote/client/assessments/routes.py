#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Collection, Ressource


# Build controllers functions.
ASSESSMENTS = Collection.as_view('assessments')
ASSESSMENT = Ressource.as_view('assessment')


# Register routes to controllers.
ROUTES = Blueprint('assessments', __name__, url_prefix='/admin')


ROUTES.add_url_rule(
    '/assessments',
    view_func=ASSESSMENTS)
ROUTES.add_url_rule(
    '/assessment',
    view_func=ASSESSMENT,
    defaults={'identifier': None})
ROUTES.add_url_rule(
    '/assessment/<int:identifier>',
    view_func=ASSESSMENT)
