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
        assessment = DATA.query(Assessment).get(identifier)
        DATA.delete(assessment)
        DATA.commit()
        return jsonify(redirect=url_for('assessments.assessments'))


class GraderController(MethodView):

    decorators = [login_required]

    @staticmethod
    def post(identifier, grader):
        """Adjust marks."""
        assessment = DATA.query(Assessment).get(identifier)
        assessment.grade(grader)
        DATA.commit()
        return jsonify(redirect=url_for('assessments.results', identifier=identifier))


class GroupView(MethodView):
    """API for group ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete an group ressource."""
        group = DATA.query(Group).get(identifier)
        DATA.delete(group)
        DATA.commit()
        return jsonify(redirect=url_for('users.groups'))


class UserView(MethodView):
    """API for user ressources."""

    decorators = [login_required]

    @staticmethod
    def delete(identifier):
        """Delete a user ressource."""
        user = DATA.query(User).get(identifier)
        DATA.delete(user)
        DATA.commit()
        return jsonify(redirect=url_for('users.users'))


def whoohoooo(data):
    print(data[0])
    return jsonify(None)


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
BLUEPRINT.add_url_rule(
    '/users/whoooohoohho',
    view_func=whoohoooo,
    methods=["POST"]
)
