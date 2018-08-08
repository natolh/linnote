#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Forms for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length, Optional


class GroupForm(Form):
    """Form for creating a group of students."""
    title = StringField('Titre', validators=[DataRequired(), Length(min=2)])
    students = FileField('Listing', validators=[Optional()])


class UserForm(Form):
    """Form for creating a user."""
    firstname = StringField('Prénom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired()])
