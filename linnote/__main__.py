#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from linnote import APP_DIR
from linnote.assessment import Test
from linnote.student import Group
from linnote.report import MetaReport
from linnote.report.composer import histogram, statistics, ranking


tests_results = list(APP_DIR.joinpath('results').glob('*.xlsx'))
GROUPS = list(Group(Group.load(gdef), gdef.stem) for gdef in Group.find())

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
        report = RankingReport(title, test, GROUPS)
        report.write()

else:
    print('--- Classement multi-épreuves ---')
    TESTS = list()

    print("Génération des classements d'épreuves")
    for results in tests_results:
        # Create and process test.
        test = Test.create(src=results)
        TESTS.append(test)
        test.adjust_marks()

        # Create and make the report.
        title = input('Titre du rapport :')
        report = RankingReport(title, test, GROUPS)
        report.write()

    print("Génération de l'interclassement")

    scale = sum(test.scale for test in TESTS)
    coefficient = sum(test.coefficient for test in TESTS)
    precision = min(test.precision for test in TESTS)

    merged = Test(scale, coefficient, precision)
    Test.aggregate_results(TESTS, merged)

    title = input('Titre du rapport :')
    report = RankingReport(title, merged, GROUPS)
    report.write()
