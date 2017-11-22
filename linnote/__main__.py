#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from locale import setlocale, LC_ALL
from linnote.configuration import LOCALE, root
from linnote.evaluation import Assessment, Test


def rank_simple(test):
    test.adjust_marks()
    test.results_to_ranking()
    test.grade()
    test.export_rankings()


setlocale(LC_ALL, LOCALE)
tests_results = list(root.joinpath('results').glob('*.xlsx'))

if not len(tests_results) > 1:
    print("Classement simple")
    test = Test.create(src=tests_results[0])
    rank_simple(test)

else:
    print("Classement multi-épreuves")
    assessment = Assessment.create()

    for n in range(0, len(tests_results)):
        test = Test.create(src=tests_results[n])
        assessment.tests.append(test)

    for test in assessment.tests:
        rank_simple(test)

    assessment.aggregate_results()
    assessment.results_to_ranking()
    assessment.grade()
    assessment.export_rankings()
