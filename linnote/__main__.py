#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from locale import setlocale, LC_ALL
from linnote.configuration import LOCALE, ROOT
from linnote.evaluation import Assessment, Test
from linnote.student import Group
from linnote.report import MetaReport
from linnote.report.composer import histogram, statistics, ranking

setlocale(LC_ALL, LOCALE)

tests_results = list(ROOT.joinpath('results').glob('*.xlsx'))
groups = list(Group(Group.load(gdef), gdef.stem) for gdef in Group.find())

RankingReport = MetaReport('RankingReport', 'test.html')
RankingReport.composers.update({'statistics': statistics, 'graph': histogram, 'ranking': ranking})


if not len(tests_results) > 1:
    print('--- Classement simple ---')
    for results in tests_results:
        # Create and process test.
        test = Test.create(src=results)
        test.adjust_marks()

        # Create and make the report.
        title = input('Titre du rapport :')
        report = RankingReport(title, test, groups)
        report.write()

else:
    print('--- Classement multi-épreuves ---')
    assessment = Assessment()

    print("Génération des classements d'épreuves")
    for results in tests_results:
        # Create and process test.
        test = Test.create(src=results)
        assessment.tests.append(test)
        test.adjust_marks()

        # Create and make the report.
        title = input('Titre du rapport :')
        report = RankingReport(title, test, groups)
        report.write()

    assessment.aggregate_results()

    print("Génération de l'interclassement")
    title = input('Titre du rapport :')
    report = RankingReport(title, assessment, groups)
    report.write()
