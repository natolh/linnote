#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from linnote import APP_DIR
from linnote.client import ranking
from linnote.student import Group


files = list(APP_DIR.joinpath('results').glob('*.xlsx'))
groups = list(Group(Group.load(gdef), gdef.stem) for gdef in Group.find())

ranking(files, groups)
