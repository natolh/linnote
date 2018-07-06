# -*- coding: utf-8 -*-

"""
Reports module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import Collection, Ressource


# Build controllers functions.
REPORTS = Collection.as_view('reports')
REPORT = Ressource.as_view('report')


# Register routes to controllers.
BLUEPRINT = Blueprint('reports', __name__, url_prefix='/admin', template_folder='templates')


BLUEPRINT.add_url_rule(
    '/reports',
    view_func=REPORTS)
BLUEPRINT.add_url_rule(
    '/report',
    view_func=REPORT,
    defaults={'identifier': None})
BLUEPRINT.add_url_rule(
    '/report/<int:identifier>',
    view_func=REPORT)
