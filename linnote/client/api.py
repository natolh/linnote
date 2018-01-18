#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Web client for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask.views import MethodView
from linnote.assessment import Assessment
from linnote.report import Report
from linnote.student import Group


API = Blueprint('api', __name__, url_prefix='/api')


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
API.add_url_rule('/assessments/<identifier>', view_func=AssessmentView.as_view('assessment'))
API.add_url_rule('/reports/<identifier>', view_func=ReportView.as_view('report'))
API.add_url_rule('/students/groups/<identifier>', view_func=GroupView.as_view('group'))
