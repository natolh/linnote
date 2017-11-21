#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from locale import setlocale, LC_ALL
from linnote.configuration import LOCALE
from linnote.evaluation import Assessment


setlocale(LC_ALL, LOCALE)
assessment = Assessment.create()
assessment.process()
