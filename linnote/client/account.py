#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Implement account related views.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .forms import UserForm, UpdatePasswordForm
from .utils import session


BLUEPRINT = Blueprint('account', __name__, url_prefix='/account')


@BLUEPRINT.route('/')
def index():
    """Index for account views."""
    return redirect(url_for('.profile'))


@BLUEPRINT.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profile endpoint."""
    form = UserForm(obj=current_user)

    if request.method == 'POST' and form.validate():
        form.populate_obj(current_user)
        session.commit()

    return render_template('account/profile.html', form=form)


@BLUEPRINT.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """Password endpoint."""
    form = UpdatePasswordForm()

    if request.method == 'POST' and form.validate():
        if form.password.data == form.password_confirm.data and current_user.is_authentic(form.old_password.data):
            current_user.set_password(form.password.data)
            session.commit()

    return render_template('account/password.html', form=form)
