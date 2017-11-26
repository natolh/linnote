#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from linnote import APP_DIR
from linnote.client import ranking
from linnote.student import Group


files = list(APP_DIR.joinpath('results').glob('*.xlsx'))
GROUPS = list(Group.load(file, file.stem) for file in Group.find())

ranking(files, GROUPS)
