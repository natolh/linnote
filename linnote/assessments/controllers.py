#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from io import StringIO
from operator import attrgetter
from statistics import mean, median
from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from matplotlib import pyplot
from sqlalchemy.orm.session import make_transient
from linnote.core.assessment import Assessment, Mark
from linnote.core.ranking import Ranking
from linnote.core.user import Group
from linnote.core.utils import DATA
from .logic import load_results
from .forms import AssessmentForm, MergeForm


class ListView(MethodView):
    """Controller for managing assessments collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the assessments collection."""
        assessments = DATA.query(Assessment).all()
        return render_template('assessments.html', assessments=assessments)


class MainView(MethodView):
    """Controller for managing an assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get(identifier):
        """Display a form for creating a new assessment."""
        if identifier:
            assessment = DATA.query(Assessment).get(identifier)
            form = AssessmentForm(obj=assessment)
            form.groups.choices = [(g.identifier, g.name) for g in DATA.query(Group).all()]
            context = dict(assessment=assessment, form=form)

        else:
            form = AssessmentForm()
            form.groups.choices = [(g.identifier, g.name) for g in DATA.query(Group).all()]
            context = dict(form=form)

        return render_template('assessment/ressource.html', **context)

    @staticmethod
    def post(identifier):
        """Create a new assessment."""
        form = AssessmentForm()
        form.groups.choices = [(g.identifier, g.name) for g in DATA.query(Group).all()]

        if form.validate() and identifier is not None:
            assessment = DATA.query(Assessment).get(identifier)
            make_transient(assessment)
            assessment.title = form.title.data
            assessment.scale = form.coefficient.data
            assessment.precision = form.precision.data

            if form.results.data:
                marks = Mark.load(request.files['results'], form.scale.data)
                assessment.add_results(marks)

                # Regenrate ranking.
                general_ranking = Ranking(assessment)
                DATA.add(general_ranking)
                subroup_rankings = []
                if form.groups.data:
                    for group in form.groups.data:
                        ranking = Ranking(assessment, group)
                        subroup_rankings.append(ranking)
                DATA.add_all(subroup_rankings)

            assessment.rescale(assessment.scale)

        elif form.validate():
            title = form.title.data
            scale = form.coefficient.data
            precision = form.precision.data

            assessment = Assessment(
                title, scale, precision=precision, creator=current_user)

            if form.results.data:
                marks = load_results(request.files['results'], form.scale.data)
                assessment.add_results(marks)

                # Create ranking.
                general_ranking = Ranking(assessment)
                DATA.add(general_ranking)
                subroup_rankings = []
                if form.groups.data:
                    for group_id in form.groups.data:
                        group = DATA.query(Group).get(group_id)
                        ranking = Ranking(assessment, group)
                        subroup_rankings.append(ranking)
                DATA.add_all(subroup_rankings)

        assessment = DATA.merge(assessment)
        DATA.commit()
        return redirect(url_for('assessments.assessment', identifier=assessment.identifier))


class ResultsView(MethodView):
    """Controller for managing assessment's results."""

    decorators = [login_required]
    template = 'assessment/results.html'

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)

    def get(self, identifier):
        """Display assessment's results."""
        data = DATA()
        assessment = data.query(Assessment).get(identifier)
        return self.render(assessment=assessment)


class MergeController(MethodView):
    """Controller for merging assessments."""

    decorators = [login_required]
    template = 'merger.html'

    @staticmethod
    def load(identifier=None):
        """Load data."""
        data = DATA()
        if not identifier:
            return data.query(Assessment).all()
        return data.query(Assessment).get(identifier)

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)

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
            DATA.add(assessment)
            DATA.commit()
        return redirect(url_for('assessments.assessments'))


class ReportController(MethodView):

    decorators = [login_required]
    template = 'assessment/report.html'

    def get(self, identifier):
        assessment = self.load(identifier)
        statistics = self.statistics(assessment)
        histograms = self.histogram(assessment)
        return self.render(assessment=assessment, statistics=statistics, histograms=histograms)

    @staticmethod
    def load(id):
        return DATA.query(Assessment).get(id)

    def render(self, **kwargs):
        return render_template(self.template, **kwargs)

    @staticmethod
    def histogram(assessment):
        for ranking in assessment.rankings:
            value = attrgetter('mark.value')
            marks = [value(rank) for rank in ranking]
        document = StringIO()
        coefficient = assessment.scale
        pyplot.figure(figsize=(6, 4))
        pyplot.hist(marks, bins=coefficient, range=(0, coefficient),
                    color=(0.80, 0.80, 0.80), histtype="stepfilled")
        pyplot.title("Répartition des notes")
        pyplot.savefig(document, format="svg")
        document.seek(0)
        yield "\n".join(document.readlines()[5:-1])

    @staticmethod
    def statistics(assessment):
        for ranking in assessment.rankings:
            marks = [rank.mark for rank in ranking]
            marks = [mark.value for mark in marks]
        yield {"size": len(marks), "maximum": max(marks, default=0),
                "minimum": min(marks, default=0),
                "mean": mean(marks) if marks else 0,
                "median": median(marks) if marks else 0}
