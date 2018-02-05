#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
API for the project.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask.views import MethodView
from linnote.core.assessment import Assessment
from linnote.core.report import Report
from linnote.core.student import Group


BLUEPRINT = Blueprint('api', __name__, url_prefix='/api')


class AssessmentView(MethodView):
    """API for assessment ressources."""

    @staticmethod
    def delete(identifier):
        """Delete an assessment ressource."""
        assessment = Assessment.fetch(identifier)
        assessment.delete(identifier)
        return "DELETED"

class ReportView(MethodView):
    """API for report ressources."""

    @staticmethod
    def delete(identifier):
        """Delete an report ressource."""
        report = Report.fetch(identifier)
        report.delete(identifier)
        return "DELETED"

class GroupView(MethodView):
    """API for group ressources."""

    @staticmethod
    def delete(identifier):
        """Delete an group ressource."""
        group = Group.fetch(identifier)
        group.delete(identifier)
        return "DELETED"


# Routes.
BLUEPRINT.add_url_rule('/assessments/<identifier>', view_func=AssessmentView.as_view('assessment'))
BLUEPRINT.add_url_rule('/reports/<identifier>', view_func=ReportView.as_view('report'))
BLUEPRINT.add_url_rule('/students/groups/<identifier>', view_func=GroupView.as_view('group'))
