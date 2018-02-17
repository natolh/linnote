#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for 'reports' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional


class ReportForm(Form):
    title = StringField('Titre', validators=[DataRequired(), Length(min=2)])
    assessments = SelectMultipleField('Épreuves', coerce=int, validators=[DataRequired()])
    subgroups = SelectMultipleField('Groupes', coerce=int, validators=[Optional()])