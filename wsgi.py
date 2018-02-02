#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
WSGI connector.

Author: Anatole Hanniet, Tutorat Santé Lyon Sud (2014-2017).
License: Mozilla Public License, see 'LICENSE.txt' for details.
"""

from linnote.client import create_app
from linnote.client import api, auth, admin


BLUEPRINTS = [api.API, auth.AUTH, admin.ADMIN]
APPLICATION = create_app('linnote', config_path='config.ini',
                         blueprints=BLUEPRINTS)
