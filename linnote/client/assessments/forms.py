#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField
from wtforms.fields import StringField, FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional


class AssessmentForm(Form):
    """Assessment form."""

    title = StringField(
        'Libellé',
        validators=[DataRequired()])
    coefficient = IntegerField(
        'Coefficient',
        default=20,
        validators=[DataRequired(), NumberRange(min=0)])
    precision = IntegerField(
        'Précision',
        default=3,
        validators=[DataRequired(), NumberRange(min=0, max=10)])
    results = FileField(
        'Fichier',
        validators=[Optional()])
    scale = FloatField(
        'Barème du fichier',
        default=20,
        validators=[Optional(), NumberRange(min=0)])
