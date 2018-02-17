#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Assessments controllers.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import render_template, request
from flask.views import MethodView
from flask_login import login_required
from linnote.client.utils import session
from .forms import AssessmentForm
from linnote.core.assessment import Assessment


class Collection(MethodView):
    """Assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessments collection."""
        assessments = session.query(Assessment).all()
        return render_template('admin/assessments.html', assessments=assessments)


class Ressource(MethodView):
    """Assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessment ressource."""
        form = AssessmentForm()
        return render_template('admin/assessment.html', form=form)

    def post(self):
        """Endpoint for assessment ressource."""
        form = AssessmentForm()
        if form.validate():
            item = Assessment(
                form.title.data,
                form.scale.data,
                form.coefficient.data,
                precision=form.precision.data,
                results=request.files['results'])
            item.rescale()
            session.merge(item)
            session.commit()

        return self.get()
