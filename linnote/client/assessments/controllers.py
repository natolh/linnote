#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Controllers for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from linnote.core.assessment import Assessment, Mark
from linnote.core.utils import WEBSESSION
from .forms import AssessmentForm


class ListView(MethodView):
    """Controller for managing assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the assessments collection."""
        session = WEBSESSION()
        assessments = session.query(Assessment).all()
        return render_template('assessments/collection.html',
                               assessments=assessments)


class MainView(MethodView):
    """Controller for managing an assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get(identifier):
        """Display a form for creating a new assessment."""
        if identifier:
            session = WEBSESSION()
            assessment = session.query(Assessment).get(identifier)
            form = AssessmentForm(obj=assessment)
            context = dict(assessment=assessment, form=form)

        else:
            form = AssessmentForm()
            context = dict(form=form)

        return render_template('assessments/assessment/ressource.html', **context)

    @staticmethod
    def post(identifier):
        """Create a new assessment."""
        session = WEBSESSION()
        form = AssessmentForm()

        if form.validate() and identifier is not None:
            assessment = session.query(Assessment).get(identifier)
            assessment.title = form.title.data
            assessment.coefficient = form.coefficient.data
            assessment.precision = form.precision.data

            if form.results.data:
                marks = Mark.load(request.files['results'], form.scale.data)
                assessment.add_results(marks)

            assessment.rescale(assessment.coefficient)
            assessment = session.merge(assessment)

        elif form.validate():
            title = form.title.data
            coefficient = form.coefficient.data
            precision = form.precision.data

            assessment = Assessment(
                title, coefficient, precision=precision, creator=current_user)

            if form.results.data:
                marks = Mark.load(request.files['results'], form.scale.data)
                assessment.add_results(marks)

            assessment = session.merge(assessment)

        session.commit()
        return redirect(url_for('assessments.assessment', identifier=assessment.identifier))


class ResultsView(MethodView):
    """Controller for managing assessment's results."""

    decorators = [login_required]

    @staticmethod
    def get(identifier):
        """Display assessment's results."""
        session = WEBSESSION()
        assessment = session.query(Assessment).get(identifier)
        return render_template('assessments/assessment/results.html',
                               assessment=assessment)
