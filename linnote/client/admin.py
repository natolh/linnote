#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Administrative client for the project.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from linnote.core.assessment import Assessment
from linnote.core.report import Report
from linnote.core.student import Group
from linnote.core.user import User
from .forms import ReportForm, GroupForm, UserForm
from .utils import session


BLUEPRINT = Blueprint('admin', __name__, url_prefix='/admin')


@BLUEPRINT.route('/')
@login_required
def home():
    """Home page."""
    return redirect(url_for('assessments.collection'), code=303)


@BLUEPRINT.route('/reports')
@login_required
def reports():
    """List of reports."""
    collection = session.query(Report).all()
    return render_template('admin/reports.html', reports=collection)


@BLUEPRINT.route('/report', defaults={'identifier': None}, methods=['GET', 'POST'])
@BLUEPRINT.route('/report/<int:identifier>')
@login_required
def report(identifier=None):
    """A report."""
    if identifier:
        item = session.query(Report).get(identifier)
        return render_template('admin/ranking.html', rep=item)

    form = ReportForm()
    form.assessments.choices = [(a.identifier, a.title) for a in session.query(Assessment).all()]
    form.subgroups.choices = [(g.identifier, g.name) for g in session.query(Group).all()]

    if request.method == 'POST' and form.validate():
        if len(form.assessments.data) > 1:
            assessments = [session.query(Assessment).get(assessment_id) for assessment_id in form.assessments.data]
            assessment = sum(assessments)
            assessment.rescale()

        else:
            assessment = session.query(Assessment).get(form.assessments.data[0])

        groups = [session.query(Group).get(group_id) for group_id in form.subgroups.data]

        rep = Report(form.title.data, assessment, groups)
        rep.build()
        session.add(rep)
        session.commit()

    return render_template('admin/report.html', form=form)


@BLUEPRINT.route('/students/groups')
@login_required
def groups():
    items = session.query(Group).all()
    return render_template('admin/groups.html', groups=items)


@BLUEPRINT.route('/students/group', methods=['GET', 'POST'])
@login_required
def group():
    form = GroupForm()
    if request.method == 'POST' and form.validate():
        g = Group.load(request.files['students'], form.title.data)
        session.merge(g)
        session.commit()
    return render_template('admin/group.html', form=form)
