#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Forms for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField
from wtforms.fields import StringField, SelectMultipleField, FormField
from wtforms.validators import DataRequired, Length, Optional


class GroupForm(Form):
    """Form for creating a group of students."""
    name = StringField('Intitulé', validators=[DataRequired(), Length(min=2)])

class UserImportationForm(Form):
    users = FileField('Listing', validators=[Optional()])


class GroupCreationForm(Form):
    name = FormField(GroupForm)
    members = FormField(UserImportationForm, label='members')


class UserForm(Form):
    """Form for creating a user."""
    firstname = StringField('Prénom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired()])
    groups = SelectMultipleField('Groupes', validators=[Optional()], coerce=int)
