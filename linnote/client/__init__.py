#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Web client for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Flask
from flask import redirect, render_template, request
from linnote import APP_DIR
from linnote.client.forms import AssessmentForm


APP = Flask('linnote')

@APP.route('/')
@APP.route('/index')
@APP.route('/home')
def home():
    """Home page."""
    return redirect('assessments', code=303)

@APP.route('/assessments')
def assessments():
    """List of assessments."""
    return render_template('assessments.html', assessments=APP_DIR.joinpath('results').glob('*.xlsx'))

@APP.route('/assessment', methods=['GET', 'POST'])
def assessment():
    """An assessment."""
    form = AssessmentForm(request.form)

    if request.method == 'POST':
        results = request.files['results']
        extension = results.filename.rsplit('.', 1)[1]
        results.save(str(APP_DIR.joinpath('results', form.title.data).with_suffix('.' + extension)))
        return redirect('assessments', code=303)

    return render_template('assessment.html', form=form)

@APP.route('/reports')
def reports():
    """List of reports."""
    return render_template('reports.html', reports=APP_DIR.joinpath('rankings').glob('*.html'))
