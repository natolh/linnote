#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for the client.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from wtforms.fields import (StringField, FileField, FloatField, IntegerField,
                            SelectMultipleField, BooleanField)


class AssessmentForm(Form): # pylint: disable=R0903
    title = StringField('Libellé')
    results = FileField('Notes')
    scale = FloatField('Barème', default=20)
    coefficient = IntegerField('Coefficient', default=20)
    precision = IntegerField('Précision', default=3)

class ReportForm(Form): # pylint: disable=R0903
    title = StringField('Titre')
    assessments = SelectMultipleField('Épreuves', coerce=str)
    subgroups = SelectMultipleField('Groupes', coerce=str)

class GroupForm(Form): # pylint: disable=R0903
    title = StringField('Titre')
    students = FileField('Listing')
