#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes for the 'assessments' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Collection, Ressource


collection_view = Collection.as_view('assessments')
ressource_view = Ressource.as_view('assessment')


ROUTES = Blueprint('assessments', __name__, url_prefix='/admin')
ROUTES.add_url_rule('/assessments', view_func=collection_view)
ROUTES.add_url_rule('/assessment', view_func=ressource_view, defaults={'identifier': None})
ROUTES.add_url_rule('/assessment/<int:identifier>', view_func=ressource_view)
