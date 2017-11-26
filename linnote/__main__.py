#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from linnote import APP_DIR
from linnote.client import rank
from linnote.student import Group


RESULTS = list(APP_DIR.joinpath('results').glob('*.xlsx'))
GROUPS = list(Group.load(file, file.stem) for file in Group.find())

rank(RESULTS, GROUPS)
