#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from locale import setlocale, LC_ALL
from linnote.configuration import LOCALE, ROOT
from linnote.evaluation import Test
from linnote.student import Group
from linnote.report import MetaReport
from linnote.report.composer import histogram, statistics

setlocale(LC_ALL, LOCALE)

tests_results = list(ROOT.joinpath('results').glob('*.xlsx'))
groups = list(Group(Group.load(gdef), gdef.stem) for gdef in Group.find())

RankingReport = MetaReport('RankingReport', 'test.html')
RankingReport.composers.update({'statistics': statistics, 'graph': histogram})

for results in tests_results:
    # Create and process test.
    test = Test.create(src=results)
    test.adjust_marks()

    # Create and make the report.
    title = input('Titre du rapport :')
    report = RankingReport(title, test, groups)
    report.write()
