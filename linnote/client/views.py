#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Controllers for the client.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template
from linnote import APP_DIR
from linnote.client import APP


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

@APP.route('/assessment', defaults={'name': None}, methods=['GET', 'POST'])
@APP.route('/assessment/<name>', methods=['GET', 'POST'])
def assessment(name=None):
    """An assessment."""
    return render_template('base.html')

@APP.route('/reports')
def reports():
    """List of reports."""
    return render_template('reports.html', reports=APP_DIR.joinpath('rankings').glob('*.html'))
