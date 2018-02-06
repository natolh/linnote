#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Administrative client for the project.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from linnote.core.assessment import Assessment
from linnote.core.report import Report
from linnote.core.student import Group
from .forms import AssessmentForm, ReportForm, GroupForm


BLUEPRINT = Blueprint('admin', __name__, url_prefix='/admin')


@BLUEPRINT.route('/')
@login_required
def home():
    """Home page."""
    return redirect(url_for('admin.assessments'), code=303)

@BLUEPRINT.route('/assessments')
@login_required
def assessments():
    """List of assessments."""
    return render_template('assessments.html', assessments=Assessment.fetch())

@BLUEPRINT.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    """An assessment."""
    form = AssessmentForm()

    if request.method == 'POST' and form.validate():
        scale = form.scale.data
        coefficient = form.coefficient.data
        precision = form.precision.data
        results = request.files['results']

        item = Assessment(scale, coefficient, precision, results)
        item.rescale()
        item.save(form.title.data)

    return render_template('assessment.html', form=form)

@BLUEPRINT.route('/reports')
@login_required
def reports():
    """List of reports."""
    return render_template('reports.html', reports=Report.fetch())

@BLUEPRINT.route('/report', defaults={'name': None}, methods=['GET', 'POST'])
@BLUEPRINT.route('/report/<name>')
@login_required
def report(name=None):
    """A report."""
    if name:
        rep = Report.fetch(name)
        return render_template('ranking.html', rep=rep)

    form = ReportForm()
    form.assessments.choices = [(a.stem, a.stem) for a in Assessment.fetch()]
    form.subgroups.choices = [(g.stem, g.stem) for g in Group.fetch()]

    if request.method == 'POST' and form.validate():
        if len(form.assessments.data) > 1:
            assessments = [Assessment.fetch(assessment) for assessment in form.assessments.data]
            scale = sum(assessment.scale for assessment in assessments)
            coefficient = sum(assessment.coefficient for assessment in assessments)
            precision = min(assessment.precision for assessment in assessments)

            assessment = Assessment(scale, coefficient, precision)
            assessment.aggregate(assessments)

        else:
            assessment = Assessment.fetch(form.assessments.data[0])

        groups = [Group.fetch(group_def) for group_def in form.subgroups.data]

        rep = Report(form.title.data, assessment, groups)
        rep.build()
        rep.save(form.title.data)

    return render_template('report.html', form=form)

@BLUEPRINT.route('/students/groups')
@login_required
def groups():
    return render_template('groups.html', groups=Group.fetch())

@BLUEPRINT.route('/students/group', methods=['GET', 'POST'])
@login_required
def group():
    form = GroupForm()
    if request.method == 'POST' and form.validate():
        g = Group.load(request.files['students'], form.title.data)
        g.save(form.title.data)
    return render_template('group.html', form=form)
