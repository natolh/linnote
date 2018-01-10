#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for the client.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from wtforms.form import Form
from wtforms.fields import StringField, FileField, DecimalField, IntegerField


class AssessmentForm(Form):
    title = StringField('Libellé')
    results = FileField('Notes')
    scale = DecimalField('Barème', places=3)
    coefficient = DecimalField('Coefficient', places=3, default=1)
    precision = IntegerField('Précision', default=3)
