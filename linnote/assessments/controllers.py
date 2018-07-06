#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from sqlalchemy.orm.session import make_transient
from linnote.core.assessment import Assessment, Mark
from linnote.core.utils import WEBSESSION
from .forms import AssessmentForm, MergeForm


class ListView(MethodView):
    """Controller for managing assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the assessments collection."""
        session = WEBSESSION()
        assessments = session.query(Assessment).all()
        return render_template('assessments.html', assessments=assessments)


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

        return render_template('assessment/ressource.html', **context)

    @staticmethod
    def post(identifier):
        """Create a new assessment."""
        session = WEBSESSION()
        form = AssessmentForm()

        if form.validate() and identifier is not None:
            assessment = session.query(Assessment).get(identifier)
            make_transient(assessment)
            assessment.title = form.title.data
            assessment.scale = form.coefficient.data
            assessment.precision = form.precision.data

            if form.results.data:
                marks = Mark.load(request.files['results'], form.scale.data)
                assessment.add_results(marks)

            assessment.rescale(assessment.scale)

        elif form.validate():
            title = form.title.data
            scale = form.coefficient.data
            precision = form.precision.data

            assessment = Assessment(
                title, scale, precision=precision, creator=current_user)

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
        return render_template('assessment/results.html',
                                assessment=assessment)


class MergeController(MethodView):
    """Controller for merging assessments."""

    decorators = [login_required]
    template = 'merger.html'

    @staticmethod
    def load(id=None):
        session = WEBSESSION()
        if not id:
            return session.query(Assessment).all()
        return session.query(Assessment).get(id)

    def render(self, **kwargs):
        return render_template(self.template, **kwargs)

    def get(self):
        assessments = self.load()
        form = MergeForm()
        form.assessments.choices = [
            (a.identifier, a.title) for a in assessments]
        return self.render(form=form)

    def post(self):
        assessments = self.load()
        form = MergeForm()
        form.assessments.choices = [
            (a.identifier, a.title) for a in assessments]

        if form.validate() and len(form.assessments.data) > 1:
            assessments = [self.load(a) for a in form.assessments.data]
            assessment = Assessment.merge(form.title.data, *assessments)
            assessment.creator = current_user
            session = WEBSESSION()
            session.add(assessment)
            session.commit()
        return redirect(url_for('assessments.assessments'))


class ReportController(MethodView):

    decorators = [login_required]
    template = 'assessment/report.html'

    def get(self, id):
        assessment = self.load(id)
        return self.render(assessment=assessment)

    @staticmethod
    def load(id):
        session = WEBSESSION()
        return session.query(Assessment).get(id)

    def render(self, **kwargs):
        return render_template(self.template, **kwargs)
