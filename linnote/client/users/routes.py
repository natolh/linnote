#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes of the 'users' app module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import GroupCollection, GroupRessource, UserCollection, UserRessource


ROUTES = Blueprint('users', __name__, url_prefix='/admin')


GroupCollection.register_to(ROUTES, name='groups')
GroupRessource.register_to(ROUTES, name='group')
UserCollection.register_to(ROUTES, name='users')
UserRessource.register_to(ROUTES, name='user')
