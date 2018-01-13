#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for the client.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from wtforms.form import Form
from wtforms.fields import (StringField, FileField, FloatField, IntegerField,
                            SelectMultipleField)


class AssessmentForm(Form): # pylint: disable=R0903
    title = StringField('Libellé')
    results = FileField('Notes')
    scale = FloatField('Barème')
    coefficient = IntegerField('Coefficient', default=1)
    precision = IntegerField('Précision', default=3)


class ReportForm(Form): # pylint: disable=R0903
    title = StringField('Titre')
    assessments = SelectMultipleField('Épreuves', coerce=str)
