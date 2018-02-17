#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for 'users' app module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length


class GroupForm(Form):
    title = StringField('Titre', validators=[DataRequired(), Length(min=2)])
    students = FileField('Listing', validators=[FileRequired()])


class UserForm(Form):
    firstname = StringField('Prénom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
