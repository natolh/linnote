#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes for the 'users' application module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import GroupCollection, GroupRessource, UserCollection, UserRessource


groups_view = GroupCollection.as_view('groups')
group_view = GroupRessource.as_view('group')
users_view = UserCollection.as_view('users')
user_view = UserRessource.as_view('user')


ROUTES = Blueprint('users', __name__, url_prefix='/admin')
ROUTES.add_url_rule('/groups', view_func=groups_view)
ROUTES.add_url_rule('/group', view_func=group_view)
ROUTES.add_url_rule('/users', view_func=users_view)
ROUTES.add_url_rule('/user', view_func=user_view)