#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Assessments routes.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Collection, Ressource


ROUTES = Blueprint('assessments', __name__, url_prefix='/admin')


Collection.register_to(ROUTES, name='collection', url='/assessments')
Ressource.register_to(ROUTES, name='ressource', url='/assessment')
