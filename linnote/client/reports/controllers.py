#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes for the 'reports' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_required
from sqlalchemy.orm import joinedload
from linnote.core.assessment import Assessment, Mark
from linnote.core.report import Report
from linnote.core.user import Group
from linnote.core.utils import WEBSESSION
from .forms import ReportForm


class Collection(MethodView):
    """Controller for managing reports collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Display the collection of reports."""
        session = WEBSESSION()
        reports = session.query(Report).all()
        return render_template('reports/collection.html', reports=reports)


class Ressource(MethodView):
    """Controller for managing a report ressource."""

    decorators = [login_required]

    @staticmethod
    def get(identifier):
        """Display a report or a form for creating a new report."""
        session = WEBSESSION()

        if identifier:
            report = session.query(Report).get(identifier)
            return render_template('reports/ranking.html', rep=report)

        form = ReportForm()
        form.assessments.choices = [(a.identifier, a.title)
                                    for a in session.query(Assessment).all()]
        form.subgroups.choices = [(g.identifier, g.name)
                                  for g in session.query(Group).all()]

        return render_template('reports/ressource.html', form=form)

    @staticmethod
    def post(identifier):
        """Create a new report."""
        session = WEBSESSION()
        form = ReportForm()
        form.assessments.choices = [(a.identifier, a.title)
                                    for a in session.query(Assessment).all()]
        form.subgroups.choices = [(g.identifier, g.name)
                                  for g in session.query(Group).all()]

        if form.validate():

            if len(form.assessments.data) > 1:
                assessments = [session.query(Assessment).get(
                    assessment_id) for assessment_id in form.assessments.data]
                assessment = sum(assessments)
                session.add(assessment)
                assessment.curve(method='top_linear')

            else:
                query = session.query(Assessment)
                query.options(joinedload(Assessment.results))
                query.options(joinedload(Mark.student))

                assessment = query.get(form.assessments.data[0])
                assessment.curve(method='top_linear')

            groups = [session.query(Group).get(group_id) for group_id in form.subgroups.data]

            report = Report(form.title.data, assessment, groups)
            report.build()
            session.add(report)
            session.commit()

        return redirect(url_for('reports.report',
                                identifier=report.identifier))
