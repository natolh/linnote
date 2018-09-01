#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Assessments module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import AssessmentsController
from .controllers import AssessmentCreationController
from .controllers import MergeController
from .controllers import AssessmentResultsController
from .controllers import AssessmentRankingsController
from .controllers import AssessmentSettingsController


# Create the module.
BLUEPRINT = Blueprint('assessments', __name__)
BLUEPRINT.url_prefix = '/assessments'
BLUEPRINT.template_folder = 'templates'

# Build views' controllers.
ASSESSMENTS = AssessmentsController.as_view('assessments')
CREATOR = AssessmentCreationController.as_view('assessment_creation')
ASSESSMENT = AssessmentResultsController.as_view('assessment')
SETTINGS = AssessmentSettingsController.as_view('settings')
RESULTS = AssessmentResultsController.as_view('results')
MERGER = MergeController.as_view('merger')
RANKINGS = AssessmentRankingsController.as_view('rankings')

# Register views' controllers routes.
BLUEPRINT.add_url_rule('', view_func=ASSESSMENTS)
BLUEPRINT.add_url_rule('/', view_func=CREATOR)
BLUEPRINT.add_url_rule('/merge', view_func=MERGER)
BLUEPRINT.add_url_rule('/<int:identifier>', view_func=ASSESSMENT)
BLUEPRINT.add_url_rule('/<int:identifier>/results', view_func=RESULTS)
BLUEPRINT.add_url_rule('/<int:identifier>/rankings', view_func=RANKINGS)
BLUEPRINT.add_url_rule('/<int:identifier>/settings', view_func=SETTINGS)
