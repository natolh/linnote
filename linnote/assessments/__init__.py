#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assessments module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import AssessmentsController, AssessmentCreationController
from .controllers import AssessmentSettingsController, AssessmentResultsController
from .controllers import MergeController
from .controllers import AssessmentRankingsController


# Build controllers functions.
LIST_VIEW = AssessmentsController.as_view('assessments')
ASSESSMENT_CREATION = AssessmentCreationController.as_view('assessment_creation')
ASSESSMENT_SETTINGS = AssessmentSettingsController.as_view('assessment')
RESULTS_VIEW = AssessmentResultsController.as_view('results')
MERGER_VIEW = MergeController.as_view('merger')
RANKINGS_VIEW = AssessmentRankingsController.as_view('rankings')


# Register routes to controllers.
BLUEPRINT = Blueprint('assessments', __name__, url_prefix='/assessments', template_folder='templates')


BLUEPRINT.add_url_rule('', view_func=LIST_VIEW)
BLUEPRINT.add_url_rule('/', view_func=ASSESSMENT_CREATION)
BLUEPRINT.add_url_rule('/<int:identifier>', view_func=ASSESSMENT_SETTINGS)
BLUEPRINT.add_url_rule('/<int:identifier>/results', view_func=RESULTS_VIEW)
BLUEPRINT.add_url_rule('/merge', view_func=MERGER_VIEW)
BLUEPRINT.add_url_rule('/<int:identifier>/rankings', view_func=RANKINGS_VIEW)
