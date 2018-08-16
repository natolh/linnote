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
from typing import List
from flask import redirect, render_template, request, url_for
from flask.views import MethodView
from flask_login import current_user, login_required
from matplotlib import pyplot
from linnote.core.assessment import Assessment
from linnote.core.ranking import Ranking
from linnote.core.user import Group
from linnote.core.utils import DATA
from .logic import load_results, rank
from .forms import AssessmentForm, MergeForm


class AssessmentsController(MethodView):
    """Controls assessments view."""

    decorators = [login_required]
    template = 'assessments.html'

    def get(self):
        """Build assessments view."""
        assessments = self.load()
        return self.render(assessments=assessments)

    @staticmethod
    def load() -> List[Assessment]:
        """Load assessments from storage."""
        data = DATA()
        assessments = data.query(Assessment).all()
        return assessments

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class AssessmentController(MethodView):
    """Commons methods for controllers of assessment's views."""

    decorators = [login_required]
    template = ''

    @staticmethod
    def load(identifier):
        """Load assessment from storage."""
        data = DATA()
        assessment = data.query(Assessment).get(identifier)
        return assessment

    @classmethod
    def render(cls, **kwargs):
        """Render a template."""
        return render_template(cls.template, **kwargs)

    @staticmethod
    def rank(assessment, groups_id=None) -> None:
        """(Re)generate rankings for the assessment."""
        data = DATA()

        # Load groups from groups_id provided in the form.
        if groups_id:
            groups = data.query(Group)
            groups = [groups.get(group_id) for group_id in groups_id]
        else:
            groups = None

        # Make rankings and persist.
        assessment.rankings = rank(assessment, groups)
        data.commit()


class AssessmentCreationController(AssessmentController):
    """Controls assessment's creation view."""

    template = 'assessment/creation.html'

    def get(self):
        """Build assessment's creation view."""
        data = DATA()
        form = AssessmentForm()
        groups = data.query(Group).all()
        form.groups.choices = [(g.identifier, g.name) for g in groups]
        return self.render(form=form)

    def post(self):
        """Create a new assessment."""
        data = DATA()
        form = AssessmentForm()
        groups = data.query(Group).all()
        form.groups.choices = [(g.identifier, g.name) for g in groups]

        if form.validate():
            title = form.title.data
            scale = form.coefficient.data
            precision = form.precision.data

            assessment = Assessment(
                title, scale, precision=precision, creator=current_user)

            if form.results.data:
                marks = load_results(request.files['results'], form.scale.data)
                assessment.add_results(marks)
                self.rank(assessment, form.groups.data)

            assessment = data.merge(assessment)
            data.commit()

        return redirect(url_for('assessments.assessment', identifier=assessment.identifier))


class AssessmentSettingsController(AssessmentController):
    """Controls assessment's settings view."""

    template = 'assessment/settings.html'

    def get(self, identifier):
        """Build assessment's settings view."""
        data = DATA()
        assessment = self.load(identifier)
        form = AssessmentForm(obj=assessment)
        groups = data.query(Group).all()
        form.groups.choices = [(g.identifier, g.name) for g in groups]
        return self.render(assessment=assessment, form=form)

    def post(self, identifier):
        """Update assessment's settings."""
        data = DATA()
        form = AssessmentForm()
        form.groups.choices = [(g.identifier, g.name) for g in data.query(Group).all()]

        if form.validate():
            assessment = self.load(identifier)
            assessment.title = form.title.data
            assessment.scale = form.coefficient.data
            assessment.precision = form.precision.data

            self.rank(assessment, form.groups.data)
            assessment.rescale(assessment.scale)
            data.commit()

        return redirect(url_for('assessments.assessment', identifier=assessment.identifier))


class ResultsView(MethodView):
    """Controls assessment's results view."""

    decorators = [login_required]
    template = 'assessment/results.html'

    def get(self, identifier):
        """Build assessment's results view."""
        data = DATA()
        assessment = data.query(Assessment).get(identifier)
        return self.render(assessment=assessment)

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class MergeController(MethodView):
    """Controls assessments merging view."""

    decorators = [login_required]
    template = 'merger.html'

    def get(self):
        """Build assessments merging view."""
        assessments = self.load()
        form = MergeForm()
        form.assessments.choices = [
            (a.identifier, a.title) for a in assessments]
        return self.render(form=form)

    def post(self):
        """Merge assessments."""
        data = DATA()
        assessments = self.load()
        form = MergeForm()
        form.assessments.choices = [
            (a.identifier, a.title) for a in assessments]

        if form.validate() and len(form.assessments.data) > 1:
            assessments = [self.load(a) for a in form.assessments.data]
            assessment = Assessment.merge(form.title.data, *assessments)
            assessment.creator = current_user
            data.add(assessment)

            # Create ranking.
            general_ranking = Ranking(assessment)
            data.add(general_ranking)

        data.commit()
        return redirect(url_for('assessments.assessments'))

    @staticmethod
    def load(identifier=None):
        """Load assessment(s) from storage."""
        data = DATA()
        if not identifier:
            return data.query(Assessment).all()
        return data.query(Assessment).get(identifier)

    @classmethod
    def render(cls, **kwargs):
        """Render the view."""
        return render_template(cls.template, **kwargs)


class AssessmentRankingsController(MethodView):
    """Controls assessment's report view."""

    template = 'assessment/rankings.html'

    def get(self, identifier):
        """Build assessment's rankings view."""
        assessment = self.load(identifier)
        statistics = self.statistics(assessment)
        histograms = self.histogram(assessment)
        return self.render(assessment=assessment, statistics=statistics, histograms=histograms)

    @staticmethod
    def load(identifier):
        """Load assessment from storage."""
        data = DATA()
        return data.query(Assessment).get(identifier)

    def render(self, **kwargs):
        """Render the view."""
        return render_template(self.template, **kwargs)

    @staticmethod
    def histogram(assessment):
        """Build an histogram of assessment's marks."""
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
            plot.close()
            document.seek(0)
            yield "\n".join(document.readlines()[5:-1])

    @staticmethod
    def statistics(assessment):
        """Build descriptive statistics of assessment's marks."""
        for ranking in assessment.rankings:
            marks = [rank.mark for rank in ranking]
            marks = [mark.value for mark in marks]
            yield {"size": len(marks), "maximum": max(marks, default=0),
                   "minimum": min(marks, default=0),
                   "mean": mean(marks) if marks else 0,
                   "median": median(marks) if marks else 0}
