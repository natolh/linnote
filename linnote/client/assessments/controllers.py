#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Controllers for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import render_template, request
from flask.views import MethodView
from flask_login import login_required
from linnote.core.assessment import Assessment
from linnote.core.utils import session
from .forms import AssessmentForm


class Collection(MethodView):
    """Controller for managing assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the assessments collection."""
        assessments = session.query(Assessment).all()
        return render_template('admin/assessments.html', assessments=assessments)


class Ressource(MethodView):
    """Controller for managing an assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display a form for creating a new assessment."""
        form = AssessmentForm()
        return render_template('admin/assessment.html', form=form)

    def post(self):
        """Create a new assessment."""
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