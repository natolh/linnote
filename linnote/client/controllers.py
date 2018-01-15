#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Web client for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import redirect, render_template, request
from linnote.assessment import Assessment
from linnote.report import Report
from linnote.student import Group
from linnote.client.forms import AssessmentForm, ReportForm, GroupForm


SITE = Blueprint('site', __name__)
GROUPS = [Group.fetch(group_def) for group_def in Group.fetch()]


@SITE.route('/')
@SITE.route('/index')
@SITE.route('/home')
def home():
    """Home page."""
    return redirect('assessments', code=303)

@SITE.route('/assessments')
def assessments():
    """List of assessments."""
    return render_template('assessments.html', assessments=Assessment.fetch())

@SITE.route('/assessment', methods=['GET', 'POST'])
def assessment():
    """An assessment."""
    form = AssessmentForm(request.form)

    if request.method == 'POST':
        scale = form.scale.data
        coefficient = form.coefficient.data
        precision = form.precision.data
        results = request.files['results']

        item = Assessment(scale, coefficient, precision, results)
        item.rescale()
        item.save(form.title.data)

        return redirect('assessments', code=303)

    return render_template('assessment.html', form=form)

@SITE.route('/reports')
def reports():
    """List of reports."""
    return render_template('reports.html', reports=Report.fetch())

@SITE.route('/report', defaults={'name': None}, methods=['GET', 'POST'])
@SITE.route('/report/<name>')
def report(name=None):
    """A report."""
    if name:
        rep = Report.fetch(name)
        return render_template('ranking.html', rep=rep)

    form = ReportForm(request.form)
    form.assessments.choices = [(a.stem, a.stem) for a in Assessment.fetch()]

    if request.method == 'POST':
        if len(form.assessments.data) > 1:
            assessments = [Assessment.fetch(assessment) for assessment in form.assessments.data]
            scale = sum(assessment.scale for assessment in assessments)
            coefficient = sum(assessment.coefficient for assessment in assessments)
            precision = min(assessment.precision for assessment in assessments)

            assessment = Assessment(scale, coefficient, precision)
            assessment.aggregate(assessments)

        else:
            assessment = Assessment.fetch(form.assessments.data[0])

        rep = Report(form.title.data, assessment, GROUPS)
        rep.build()
        rep.save(form.title.data)
        return render_template('ranking.html', rep=rep)

    return render_template('report.html', form=form)

@SITE.route('/students/groups')
def groups():
    return render_template('groups.html', groups=Group.fetch())

@SITE.route('/students/group', methods=['GET', 'POST'])
def group():
    form = GroupForm(request.form)
    if request.method == 'POST':
        g = Group.load(request.files['students'], form.title.data)
        g.save(form.title.data)
    return render_template('group.html', form=form)
