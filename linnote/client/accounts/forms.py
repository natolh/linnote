#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Accounts forms.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask_wtf import FlaskForm as Form
from wtforms.fields import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(Form):
    """Form for login users."""
    identifier = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])


class PasswordForm(Form):
    """Form for editing the user's password."""
    old_password = PasswordField(
        'Ancien mot de passe',
        validators=[DataRequired()])
    password = PasswordField(
        'Nouveau mot de passe',
        validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('Confirmer')


class ProfileForm(Form):
    """Form for editing the user's profile."""
    firstname = StringField('Prénom', validators=[DataRequired()])
    lastname = StringField('Nom', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired()])
