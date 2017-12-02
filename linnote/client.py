#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Command Line Tool for the application.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""


import click
from linnote.assessment import Assessment
from linnote.report import Report


def rank(files, groups, precision=3, merge=True):
    """Rank command establish a ranking report for an assessment."""
    assessments = list()

    click.echo("*** Création des rapports d'épreuves ***")
    for file in files:
        click.echo(file.stem)

        title = click.prompt('Titre du rapport')
        scale = click.prompt('Barème', type=float)
        coefficient = click.prompt('Coefficient', type=int)

        assessment = Assessment(scale, coefficient, precision, results=file)
        assessment.rescale()

        report = Report(title, assessment, groups)
        report.write()

        assessments.append(assessment)

    click.echo("*** Création de la synthèse ***")
    if merge:
        title = click.prompt('Titre du rapport')
        scale = sum(assessment.scale for assessment in assessments)
        coefficient = sum(assessment.coefficient for assessment in assessments)

        assessment = Assessment(scale, coefficient, precision)
        assessment.aggregate(assessments)

        report = Report(title, assessment, groups)
        report.write()
