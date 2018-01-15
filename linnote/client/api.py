#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Web client for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import make_response
from linnote.assessment import Assessment
from linnote.report import Report
from linnote.student import Group


API = Blueprint('api', __name__, url_prefix='/api')


@API.route('/assessment/<name>', methods=['DELETE'])
def assessment(name):
    """API endpoint for assessment."""
    i = Assessment.fetch(name)
    i.delete(name)
    return make_response('DELETE has success', 200, None)

@API.route('/report/<name>', methods=['DELETE'])
def report(name):
    """API endpoint for report."""
    i = Report.fetch(name)
    i.delete(name)
    return make_response('DELETE has success', 200, None)

@API.route('/students/groups/<name>', methods=['DELETE'])
def group(name):
    """API endpoint for students group."""
    i = Group.fetch(name)
    i.delete(name)
    return make_response('DELETE has success', 200, None)
