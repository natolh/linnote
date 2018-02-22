#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import ListView, MainView, ResultsView


# Build controllers functions.
LIST_VIEW = ListView.as_view('assessments')
MAIN_VIEW = MainView.as_view('assessment')
RESULTS_VIEW = ResultsView.as_view('results')


# Register routes to controllers.
ROUTES = Blueprint('assessments', __name__, url_prefix='/admin')


ROUTES.add_url_rule(
    '/assessments',
    view_func=LIST_VIEW)
ROUTES.add_url_rule(
    '/assessment',
    view_func=MAIN_VIEW,
    defaults={'identifier': None})
ROUTES.add_url_rule(
    '/assessment/<int:identifier>',
    view_func=MAIN_VIEW)
ROUTES.add_url_rule(
    '/assessment/<int:identifier>/results',
    view_func=RESULTS_VIEW)
