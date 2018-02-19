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
        return render_template('assessments/collection.html',
                               assessments=assessments)


class Ressource(MethodView):
    """Controller for managing an assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get(identifier):
        """Display a form for creating a new assessment."""
        if identifier:
            assessment = session.query(Assessment).get(identifier)
            form = AssessmentForm(obj=assessment)
            context = dict(assessment=assessment, form=form)
        
        else:
            form = AssessmentForm()
            context = dict(form=form)
        
        return render_template('assessments/ressource.html', **context)

    def post(self, identifier):
        """Create a new assessment."""
        form = AssessmentForm()

        if form.validate() and identifier:
            assessment = session.query(Assessment).get(identifier)
            assessment.title = form.title.data
            assessment.scale = form.scale.data
            assessment.coefficient = form.coefficient.data
            assessment.precision = form.precision.data

            if form.results.data:
                assessment.load(request.files['results'])

        elif form.validate():
            assessment = Assessment(form.title.data, form.scale.data, 
                                    form.coefficient.data,
                                    precision=form.precision.data,
                                    results=request.files['results'])
        
        assessment.rescale()
        session.merge(assessment)
        session.commit()
        return self.get(identifier)
