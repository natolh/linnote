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
from .utils import session


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
    items = session.query(Assessment).all()
    return render_template('admin/assessments.html', assessments=items)

@BLUEPRINT.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    """An assessment."""
    form = AssessmentForm()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        scale = form.scale.data
        coefficient = form.coefficient.data
        precision = form.precision.data
        results = request.files['results']

        item = Assessment(title, scale, coefficient, precision, results)
        session.merge(item)
        session.commit()

    return render_template('admin/assessment.html', form=form)

@BLUEPRINT.route('/reports')
@login_required
def reports():
    """List of reports."""
    return render_template('admin/reports.html', reports=Report.fetch())

@BLUEPRINT.route('/report', defaults={'name': None}, methods=['GET', 'POST'])
@BLUEPRINT.route('/report/<name>')
@login_required
def report(name=None):
    """A report."""
    if name:
        rep = Report.fetch(name)
        return render_template('admin/ranking.html', rep=rep)

    form = ReportForm()
    form.assessments.choices = [(a.identifier, a.title) for a in session.query(Assessment).all()]
    form.subgroups.choices = [(g.identifier, g.name) for g in session.query(Group).all()]

    if request.method == 'POST' and form.validate():
        if len(form.assessments.data) > 1:
            assessments = [session.query(Assessment).get(assessment_id) for assessment_id in form.assessments.data]
            scale = sum(assessment.scale for assessment in assessments)
            coefficient = sum(assessment.coefficient for assessment in assessments)
            precision = min(assessment.precision for assessment in assessments)

            assessment = Assessment(scale, coefficient, precision)
            assessment.aggregate(assessments)

        else:
            assessment = session.query(Assessment).get(form.assessments.data[0])

        groups = [session.query(Group).get(group_id) for group_id in form.subgroups.data]

        rep = Report(form.title.data, assessment, groups)
        rep.build()
        rep.save(form.title.data)

    return render_template('admin/report.html', form=form)

@BLUEPRINT.route('/students/groups')
@login_required
def groups():
    items = session.query(Group).all()
    return render_template('admin/groups.html', groups=items)

@BLUEPRINT.route('/students/group', methods=['GET', 'POST'])
@login_required
def group():
    form = GroupForm()
    if request.method == 'POST' and form.validate():
        g = Group.load(request.files['students'], form.title.data)
        session.merge(g)
        session.commit()
    return render_template('admin/group.html', form=form)
