#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from linnote import APP_DIR
from linnote.client import rank
from linnote.student import Group


RESULTS = list(APP_DIR.joinpath('results').glob('*.xlsx'))

GROUPS = list()
for group_definition in Group.find(APP_DIR.joinpath('groups')):
    group = Group.load(group_definition)
    GROUPS.append(group)

if RESULTS:
    rank(RESULTS, GROUPS)

else:
    print("Aucun fichier de résultats...")
