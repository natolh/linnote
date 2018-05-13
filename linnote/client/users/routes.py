#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Routes for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import GroupCollection, GroupRessource, UserCollection, UserRessource


# Build controllers functions.
GROUPS = GroupCollection.as_view('groups')
GROUP = GroupRessource.as_view('group')
USERS = UserCollection.as_view('users')
USER = UserRessource.as_view('user')


# Register routes to controllers.
ROUTES = Blueprint('users', __name__, url_prefix='/admin')


ROUTES.add_url_rule('/groups', view_func=GROUPS)
ROUTES.add_url_rule('/group', view_func=GROUP)
ROUTES.add_url_rule('/users', view_func=USERS)
ROUTES.add_url_rule('/user', view_func=USER)
