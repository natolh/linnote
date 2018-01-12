#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Web client for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from pickle import dump, load
from flask import Flask
from flask import redirect, render_template, request
from linnote import APP_DIR
from linnote.assessment import Assessment
from linnote.report import Report
from linnote.student import Group
from linnote.client.forms import AssessmentForm, ReportForm


APP = Flask('linnote')
GROUPS = list()
for group_definition in Group.find(APP_DIR.joinpath('groups')):
    group = Group.load(group_definition)
    GROUPS.append(group)

@APP.route('/')
@APP.route('/index')
@APP.route('/home')
def home():
    """Home page."""
    return redirect('assessments', code=303)

@APP.route('/assessments')
def assessments():
    """List of assessments."""
    return render_template('assessments.html', assessments=APP_DIR.joinpath('results').glob('[!.]*'))

@APP.route('/assessment', methods=['GET', 'POST'])
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

        dump(item, APP_DIR.joinpath('results', form.title.data).open('wb'), -1)
        return redirect('assessments', code=303)

    return render_template('assessment.html', form=form)

@APP.route('/reports')
def reports():
    """List of reports."""
    return render_template('reports.html', reports=APP_DIR.joinpath('rankings').glob('[!.]*'))

@APP.route('/report', defaults={'name': None}, methods=['GET', 'POST'])
@APP.route('/report/<name>')
def report(name=None):
    """A report."""
    if name:
        rep = Report.load(name)
        return render_template('ranking.html', rep=rep)

    form = ReportForm(request.form)
    form.assessments.choices = [(a.stem, a.stem) for a in APP_DIR.joinpath('results').glob('[!.]*')]

    if request.method == 'POST':
        if len(form.assessments.data) > 1:
            assessments = [load(APP_DIR.joinpath('results', assessment).open('rb')) for assessment in form.assessments.data]
            scale = sum(assessment.scale for assessment in assessments)
            coefficient = sum(assessment.coefficient for assessment in assessments)
            precision = min(assessment.precision for assessment in assessments)

            assessment = Assessment(scale, coefficient, precision)
            assessment.aggregate(assessments)

        else:
            assessment = load(APP_DIR.joinpath('results', form.assessments.data[0]).open('rb'))

        rep = Report(form.title.data, assessment, GROUPS)
        rep.build()
        rep.save()
        return render_template('ranking.html', rep=rep)

    return render_template('report.html', form=form)
