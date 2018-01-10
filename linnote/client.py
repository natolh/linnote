#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Command Line Tool for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


from flask import Flask
from flask import render_template


APP = Flask('linnote')


@APP.route('/')
@APP.route('/index')
@APP.route('/home')
def home():
    """Home page."""
    return render_template('base.html')
