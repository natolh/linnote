#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assessments module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import ListView, MainView, ResultsView, MergeController
from .controllers import ReportController


# Build controllers functions.
LIST_VIEW = ListView.as_view('assessments')
MAIN_VIEW = MainView.as_view('assessment')
RESULTS_VIEW = ResultsView.as_view('results')
MERGER_VIEW = MergeController.as_view('merger')
REPORT_VIEW = ReportController.as_view('report')


# Register routes to controllers.
BLUEPRINT = Blueprint('assessments', __name__, url_prefix='/admin', template_folder='templates')


BLUEPRINT.add_url_rule(
    '/assessments',
    view_func=LIST_VIEW)
BLUEPRINT.add_url_rule(
    '/assessment',
    view_func=MAIN_VIEW,
    defaults={'identifier': None})
BLUEPRINT.add_url_rule(
    '/assessment/<int:identifier>',
    view_func=MAIN_VIEW)
BLUEPRINT.add_url_rule(
    '/assessment/<int:identifier>/results',
    view_func=RESULTS_VIEW)
BLUEPRINT.add_url_rule(
    '/assessments/merge',
    view_func=MERGER_VIEW)
BLUEPRINT.add_url_rule(
    '/assessment/<int:identifier>/report',
    view_func=REPORT_VIEW)
