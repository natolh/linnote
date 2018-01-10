#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Command Line Tool for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


from flask import Flask
from flask import redirect, render_template


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
    return render_template('base.html')

@APP.route('/reports')
def reports():
    """List of reports."""
    return render_template('base.html')
