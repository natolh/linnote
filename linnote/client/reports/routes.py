#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes for the 'reports' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Collection, Ressource


# Build controllers functions.
REPORTS = Collection.as_view('reports')
REPORT = Ressource.as_view('report')


# Register routes to controllers.
ROUTES = Blueprint('reports', __name__, url_prefix='/admin')


ROUTES.add_url_rule(
    '/reports',
    view_func=REPORTS)
ROUTES.add_url_rule(
    '/report',
    view_func=REPORT,
    defaults={'identifier': None})
ROUTES.add_url_rule(
    '/report/<int:identifier>',
    view_func=REPORT)
