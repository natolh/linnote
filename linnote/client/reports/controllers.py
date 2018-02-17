#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes for the 'reports' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import render_template
from flask.views import MethodView
from flask_login import login_required
from linnote.client.utils import session
from linnote.core.assessment import Assessment
from linnote.core.report import Report
from linnote.core.user import Group
from .forms import ReportForm



class Collection(MethodView):
    """Groups collection."""

    decorators = [login_required]

    @staticmethod
    def get():
        """Endpoint for assessments collection."""
        reports = session.query(Report).all()
        return render_template('admin/reports.html', reports=reports)


class Ressource(MethodView):
    """Assessment ressource."""

    decorators = [login_required]

    @staticmethod
    def get(identifier):
        """Endpoint for assessment ressource."""
        if identifier:
            report = session.query(Report).get(identifier)
            return render_template('admin/ranking.html', rep=report)

        form = ReportForm()
        form.assessments.choices = [(a.identifier, a.title) for a in session.query(Assessment).all()]
        form.subgroups.choices = [(g.identifier, g.name) for g in session.query(Group).all()]

        return render_template('admin/report.html', form=form)

    def post(self, identifier):
        """Endpoint for assessment ressource."""
        form = ReportForm()
        form.assessments.choices = [(a.identifier, a.title) for a in session.query(Assessment).all()]
        form.subgroups.choices = [(g.identifier, g.name) for g in session.query(Group).all()]

        if form.validate():

            if len(form.assessments.data) > 1:
                assessments = [session.query(Assessment).get(assessment_id) for assessment_id in form.assessments.data]
                assessment = sum(assessments)
                assessment.rescale()

            else:
                assessment = session.query(Assessment).get(form.assessments.data[0])

            groups = [session.query(Group).get(group_id) for group_id in form.subgroups.data]

            report = Report(form.title.data, assessment, groups)
            report.build()
            session.add(report)
            session.commit()

        return self.get(identifier)