#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
API for the project.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask.views import MethodView
from flask_login import login_required
from linnote.core.assessment import Assessment
from linnote.core.report import Report
from linnote.core.user import User, Group
from .utils import session


BLUEPRINT = Blueprint('api', __name__, url_prefix='/api')


class AssessmentView(MethodView):
    """API for assessment ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete an assessment ressource."""
        assessment = session.query(Assessment).get(identifier)
        session.delete(assessment)
        session.commit()
        return "DELETED"


class ReportView(MethodView):
    """API for report ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete an report ressource."""
        report = session.query(Report).get(identifier)
        session.delete(report)
        session.commit()
        return "DELETED"


class GroupView(MethodView):
    """API for group ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete an group ressource."""
        group = session.query(Group).get(identifier)
        session.delete(group)
        session.commit()
        return "DELETED"


class UserView(MethodView):
    """API for user ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete a user ressource."""
        user = session.query(User).get(identifier)
        session.delete(user)
        session.commit()
        return 'DELETED'


# Routes.
BLUEPRINT.add_url_rule('/assessments/<int:identifier>', view_func=AssessmentView.as_view('assessment'))
BLUEPRINT.add_url_rule('/reports/<identifier>', view_func=ReportView.as_view('report'))
BLUEPRINT.add_url_rule('/students/groups/<int:identifier>', view_func=GroupView.as_view('group'))
BLUEPRINT.add_url_rule('/users/<int:identifier>', view_func=UserView.as_view('user'))
