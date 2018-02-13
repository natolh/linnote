#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Forms for the client.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from flask_wtf.file import FileField, FileRequired
from wtforms.fields import (StringField, FloatField, IntegerField,
                            SelectMultipleField, PasswordField)
from wtforms.validators import (DataRequired, Length, Optional, NumberRange,
                                EqualTo)


class AssessmentForm(Form): # pylint: disable=R0903
    title = StringField('Libellé', validators=[DataRequired(), Length(min=2)])
    results = FileField('Notes', validators=[FileRequired()])
    scale = FloatField('Barème', default=20, validators=[DataRequired(), NumberRange(min=0)])
    coefficient = IntegerField('Coefficient', default=20, validators=[DataRequired(), NumberRange(min=0)])
    precision = IntegerField('Précision', default=3, validators=[DataRequired(), NumberRange(min=0, max=10)])

class ReportForm(Form): # pylint: disable=R0903
    title = StringField('Titre', validators=[DataRequired(), Length(min=2)])
    assessments = SelectMultipleField('Épreuves', coerce=int, validators=[DataRequired()])
    subgroups = SelectMultipleField('Groupes', coerce=int, validators=[Optional()])

class GroupForm(Form): # pylint: disable=R0903
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
