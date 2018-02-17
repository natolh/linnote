#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for the client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import StringField, SelectMultipleField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, EqualTo


class ReportForm(Form):
    title = StringField('Titre', validators=[DataRequired(), Length(min=2)])
    assessments = SelectMultipleField('Épreuves', coerce=int, validators=[DataRequired()])
    subgroups = SelectMultipleField('Groupes', coerce=int, validators=[Optional()])

class GroupForm(Form):
    title = StringField('Titre', validators=[DataRequired(), Length(min=2)])
    students = FileField('Listing', validators=[FileRequired()])

class LoginForm(Form):
    identifier = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

class UserForm(Form):
    firstname = StringField('Prénom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])

class UpdatePasswordForm(Form):
    old_password = PasswordField('Ancien mot de passe', validators=[DataRequired()])
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('Confirmer')
