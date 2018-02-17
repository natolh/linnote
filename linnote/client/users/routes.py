#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Routes of the 'users' app module.

Author: Anatole Hanniet, 2016-2018.
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from flask import Blueprint
from .controllers import UserCollection, UserRessource


ROUTES = Blueprint('users', __name__, url_prefix='/admin')


UserCollection.register_to(ROUTES, name='users')
UserRessource.register_to(ROUTES, name='user')
