#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Web services module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint, jsonify, url_for
from flask.views import MethodView
from flask_login import login_required
from linnote.core.assessment import Assessment
from linnote.core.user import User, Group
from linnote.core.utils import DATA


BLUEPRINT = Blueprint('api', __name__, url_prefix='/api')


class AssessmentView(MethodView):
    """API for assessment ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete an assessment ressource."""
        data = DATA()
        assessment = data.query(Assessment).get(identifier)
        data.delete(assessment)
        data.commit()
        return jsonify(redirect=url_for('assessments.assessments'))


class GraderController(MethodView):
    """API for enabling / removing mark adjustments."""

    decorators = [login_required]

    @staticmethod
    def post(identifier, grader):
        """Adjust marks."""
        data = DATA()
        assessment = data.query(Assessment).get(identifier)
        assessment.grade(grader)
        data.commit()
        return jsonify(redirect=url_for('assessments.results', identifier=identifier))


class GroupView(MethodView):
    """API for group ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete an group ressource."""
        data = DATA()
        group = data.query(Group).get(identifier)
        data.delete(group)
        data.commit()
        return jsonify(redirect=url_for('users.groups'))


class UserView(MethodView):
    """API for user ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete a user ressource."""
        data = DATA()
        user = data.query(User).get(identifier)
        data.delete(user)
        data.commit()
        return jsonify(redirect=url_for('users.users'))


# Register routes to controllers.
BLUEPRINT.add_url_rule(
    '/assessments/<int:identifier>',
    view_func=AssessmentView.as_view('assessment'))
BLUEPRINT.add_url_rule(
    '/assessments/<int:identifier>/marks/grader/<grader>',
    view_func=GraderController.as_view('grade'))
BLUEPRINT.add_url_rule(
    '/students/groups/<int:identifier>',
    view_func=GroupView.as_view('group'))
BLUEPRINT.add_url_rule(
    '/users/<int:identifier>',
    view_func=UserView.as_view('user'))
